from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from auth import RateLimiter
from config import settings
from detectors.red_flag import RedFlagDetector


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
rate_limiter = RateLimiter()


@app.post("/classify")
async def classify(request: Request, payload: ClassifyRequest):
    client_ip = request.client.host
    allowed, message = rate_limiter.check_limit(client_ip)

    if not allowed:
        return JSONResponse({"error": message}, status_code=429)

    rate_limiter.increment(client_ip)

    result = await detector.classify(payload.case_text)
    rate_limiter.add_cost(client_ip, result.get("cost_usd", 0.0))

    return {
        "esi_level": result["esi"],
        "confidence": result["confidence"],
        "reason": result["reason"],
        "intermediate": {
            "red_flags": result.get("flags", []),
            "severity": result.get("severity_score", 0.0),
            "has_red_flags": result.get("has_red_flags", False),
        },
        "cost": {
            "prompt_tokens": result.get("prompt_tokens", 0),
            "completion_tokens": result.get("completion_tokens", 0),
            "total_tokens": result.get("total_tokens", 0),
            "estimated_cost_usd": result.get("cost_usd", 0.0),
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
