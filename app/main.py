from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from auth import RateLimiter
from config import settings
from detectors.red_flag import RedFlagDetector
from detectors.vital_signal import VitalSignalDetector
from detectors.resource_inference import ResourceInferenceDetector
from detectors.handbook_verification import HandbookVerificationDetector
from api.routes import admin_rag


class ClassifyRequest(BaseModel):
    case_text: str = Field(..., min_length=1, description="Patient case description")


app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = RedFlagDetector()
vital_detector = VitalSignalDetector()
resource_detector = ResourceInferenceDetector()
handbook_detector = HandbookVerificationDetector()
rate_limiter = RateLimiter()


@app.post("/classify")
async def classify(request: Request, payload: ClassifyRequest):
    client_ip = request.client.host
    allowed, message = rate_limiter.check_limit(client_ip)

    if not allowed:
        return JSONResponse({"error": message}, status_code=429)

    rate_limiter.increment(client_ip)

    red_flag = await detector.classify(payload.case_text)
    vital = await vital_detector.assess(payload.case_text)
    resources = await resource_detector.infer(payload.case_text)

    # Simple pipeline logic (temporary until full multi-layer orchestration)
    if red_flag.get("has_red_flags"):
        esi_level = 2
        reason = "Red flags detected"
        confidence = red_flag.get("confidence", 0.7)
    else:
        resource_count = resources.get("resource_count", 0)
        if resource_count >= 2:
            esi_level = 3
            reason = "Requires 2+ resources"
        elif resource_count == 1:
            esi_level = 4
            reason = "Requires 1 resource"
        else:
            esi_level = 5
            reason = "No resources required"
        confidence = 0.6

    # Escalate if vitals critical
    if vital.get("critical"):
        esi_level = min(esi_level, 2)
        reason = "Critical vital signs"
        confidence = max(confidence, 0.75)

    handbook = await handbook_detector.verify(esi_level, payload.case_text)
    rate_limiter.add_cost(client_ip, red_flag.get("cost_usd", 0.0))

    return {
        "esi_level": esi_level,
        "confidence": confidence,
        "reason": reason,
        "intermediate": {
            "red_flags": red_flag.get("flags", []),
            "severity": red_flag.get("severity_score", 0.0),
            "has_red_flags": red_flag.get("has_red_flags", False),
            "vitals": vital,
            "resources": resources,
            "handbook_verification": handbook,
        },
        "cost": {
            "prompt_tokens": red_flag.get("prompt_tokens", 0),
            "completion_tokens": red_flag.get("completion_tokens", 0),
            "total_tokens": red_flag.get("total_tokens", 0),
            "estimated_cost_usd": red_flag.get("cost_usd", 0.0),
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

