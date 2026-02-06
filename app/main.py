from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import re

from pydantic import BaseModel, Field

from auth import RateLimiter
from config import settings
from detectors.red_flag import RedFlagDetector
from detectors.extraction import ExtractionDetector
from detectors.vital_signal import VitalSignalDetector
import asyncio
from detectors.malicious_input import MaliciousInputDetector, LLMMaliciousInputDetector
from detectors.resource_inference import ResourceInferenceDetector
from detectors.handbook_verification import HandbookVerificationDetector
from detectors.final_decision import FinalDecisionDetector
from llm_router import LLMRouter
from api.routes import admin_rag


class ClassifyRequest(BaseModel):
    case_text: str = Field(..., min_length=1, description="Patient case description")
    model: Optional[str] = Field(
        default=None,
        description="LLM model override (use 'auto' or omit for routing)",
    )


app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = RedFlagDetector()
extraction_detector = ExtractionDetector()
vital_detector = VitalSignalDetector()
resource_detector = ResourceInferenceDetector()
handbook_detector = HandbookVerificationDetector()
final_detector = FinalDecisionDetector()
router = LLMRouter()
rate_limiter = RateLimiter()
malicious_detector = MaliciousInputDetector()
malicious_llm_detector = LLMMaliciousInputDetector()


@app.post("/classify")
async def classify(request: Request, payload: ClassifyRequest):
    client_ip = request.client.host
    allowed, message = rate_limiter.check_limit(client_ip)

    if not allowed:
        return JSONResponse({"error": message}, status_code=429)

    rate_limiter.increment(client_ip)

    malicious_check, malicious_llm_check = await asyncio.gather(
        asyncio.to_thread(malicious_detector.analyze, payload.case_text),
        malicious_llm_detector.analyze(payload.case_text),
    )
    sanitized_case_text = malicious_check.get("sanitized_text") or payload.case_text

    if malicious_llm_check.get("enabled") and malicious_llm_check.get("is_malicious"):
        if malicious_llm_check.get("can_sanitize") and malicious_llm_check.get("sanitized_text"):
            sanitized_case_text = malicious_llm_check["sanitized_text"]
        else:
            return JSONResponse(
                {
                    "error": "Potential prompt injection detected. Please remove instruction-like content and resubmit.",
                    "malicious_input": {**malicious_check, "llm": malicious_llm_check},
                },
                status_code=400,
            )

    extracted = extraction_detector.extract(sanitized_case_text)
    model_override = payload.model if payload.model and payload.model != "auto" else None
    red_flag_model = (
        model_override or router.select_red_flag_model(sanitized_case_text, extracted)
    )
    red_flag = await detector.classify(sanitized_case_text, extracted, model=red_flag_model)
    vital = await vital_detector.assess(sanitized_case_text, extracted)
    resources = await resource_detector.infer(sanitized_case_text, extracted)

    # Simple pipeline logic (temporary scoring passed into LLM final decision)
    if red_flag.get("has_red_flags"):
        preliminary_esi = 2
        preliminary_reason = "Red flags detected"
    else:
        resource_count = resources.get("resource_count", 0)
        if resource_count >= 2:
            preliminary_esi = 3
            preliminary_reason = "Requires 2+ resources"
        elif resource_count == 1:
            preliminary_esi = 4
            preliminary_reason = "Requires 1 resource"
        else:
            preliminary_esi = 5
            preliminary_reason = "No resources required"

    # Escalate if vitals critical
    if vital.get("critical"):
        preliminary_esi = min(preliminary_esi, 2)
        preliminary_reason = "Critical vital signs"

    final_context = {
        "esi_level": preliminary_esi,
        "preliminary_reason": preliminary_reason,
        "extraction": extracted,
        "red_flags": red_flag,
        "vitals": vital,
        "resources": resources,
    }

    final_model = (
        model_override
        or router.select_final_decision_model(sanitized_case_text, final_context)
    )
    final_decision = await final_detector.decide(sanitized_case_text, final_context, model=final_model)
    rate_limiter.add_cost(client_ip, red_flag.get("cost_usd", 0.0))

    final_esi_level_raw = final_decision.get("esi", preliminary_esi)
    if isinstance(final_esi_level_raw, int):
        final_esi_level = final_esi_level_raw
    elif isinstance(final_esi_level_raw, str):
        match = re.search(r"\d", final_esi_level_raw)
        final_esi_level = int(match.group()) if match else preliminary_esi
    else:
        final_esi_level = preliminary_esi

    handbook = await handbook_detector.verify(final_esi_level, sanitized_case_text)
    final_context["handbook_verification"] = handbook

    layer_costs = {
        "malicious": float(malicious_llm_check.get("cost_usd", 0.0) or 0.0),
        "red_flag": float(red_flag.get("cost_usd", 0.0) or 0.0),
        "final_decision": float(final_decision.get("cost_usd", 0.0) or 0.0),
        "vitals": 0.0,
        "resources": float(resources.get("cost_usd", 0.0) or 0.0),
        "handbook": 0.0,
    }
    total_cost = sum(layer_costs.values())

    return {
        "esi_level": final_esi_level,
        "confidence": final_decision.get("confidence", 0.6),
        "reason": final_decision.get("reason", preliminary_reason),
        "intermediate": {
            "extraction": extracted,
            "red_flags": red_flag.get("flags", []),
            "red_flag_layer": red_flag,
            "severity": red_flag.get("severity_score", 0.0),
            "has_red_flags": red_flag.get("has_red_flags", False),
            "vitals": vital,
            "resources": resources,
            "malicious_input": {
                **malicious_check,
                "llm": malicious_llm_check,
            },
            "handbook_verification": handbook,
            "final_decision": final_decision,
            "routing": {
                "mode": "fixed" if model_override else "auto",
                "red_flag_model": red_flag.get("model", red_flag_model),
                "final_decision_model": final_decision.get("model", final_model),
            },
            "layer_costs": layer_costs,
        },
        "cost": {
            "prompt_tokens": (
                malicious_llm_check.get("prompt_tokens", 0)
                + red_flag.get("prompt_tokens", 0)
                + final_decision.get("prompt_tokens", 0)
            ),
            "completion_tokens": (
                malicious_llm_check.get("completion_tokens", 0)
                + red_flag.get("completion_tokens", 0)
                + final_decision.get("completion_tokens", 0)
            ),
            "total_tokens": (
                malicious_llm_check.get("total_tokens", 0)
                + red_flag.get("total_tokens", 0)
                + final_decision.get("total_tokens", 0)
            ),
            "estimated_cost_usd": total_cost,
            "budget_remaining_usd": rate_limiter.get_remaining_budget(client_ip),
        },
        "queries_remaining": rate_limiter.get_remaining(client_ip),
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "triage-classifier"}


@app.get("/info")
async def info():
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "environment": "mvp",
        "model": settings.LLM_MODEL,
        "rate_limit": settings.RATE_LIMIT_PER_DAY,
        "free_tier_daily_budget_usd": settings.FREE_TIER_DAILY_BUDGET_USD,
    }


# Include admin RAG configuration routes
app.include_router(admin_rag.router, tags=["admin"])

