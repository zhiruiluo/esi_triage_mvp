import json
from typing import Any, Dict

from openai import AsyncOpenAI

from config import settings


SYSTEM_PROMPT = """You are an ESI (Emergency Severity Index) triage expert.
Identify if this case has RED FLAGS that would classify as ESI-2.

ESI-2 (Potentially Life-Threatening):
- Chest pain or shortness of breath
- Severe hemorrhage or shock
- Altered mental status
- Severe allergic reaction
- Severe hypotension/hypertension
- Uncontrolled seizure
- Severe respiratory distress
- Life-threatening trauma

Return JSON:
{
  \"has_red_flags\": true/false,
  \"flags_detected\": [\"flag1\", \"flag2\"],
  \"severity_score\": 0.0-1.0,
  \"esi_level\": 1-5,
  \"confidence\": 0.0-1.0,
  \"reasoning\": \"brief explanation\"
}
"""


class RedFlagDetector:
    def __init__(self) -> None:
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        
        self.client = AsyncOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
        )

    async def classify(self, case_text: str) -> Dict[str, Any]:
        if not settings.OPENROUTER_API_KEY:
            return {
                "esi": 3,
                "confidence": 0.0,
                "reason": "Missing OPENROUTER_API_KEY",
                "flags": [],
                "severity_score": 0.0,
                "has_red_flags": False,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "cost_usd": 0.0,
            }

        try:
            response = await self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Case: {case_text}"},
                ],
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
                response_format={"type": "json_object"},
            )

            result = json.loads(response.choices[0].message.content)
            usage = response.usage
            prompt_tokens = usage.prompt_tokens if usage else 0
            completion_tokens = usage.completion_tokens if usage else 0
            total_tokens = usage.total_tokens if usage else 0
            cost_usd = (
                (prompt_tokens / 1000.0) * settings.COST_PER_1K_INPUT
                + (completion_tokens / 1000.0) * settings.COST_PER_1K_OUTPUT
            )

            flags = result.get("flags_detected", [])
            return {
                "esi": result.get("esi_level", 3),
                "confidence": result.get("confidence", 0.0),
                "reason": result.get("reasoning", ""),
                "flags": flags,
                "severity_score": result.get("severity_score", 0.0),
                "has_red_flags": result.get("has_red_flags", bool(flags)),
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "cost_usd": cost_usd,
            }
        except Exception as exc:
            return {
                "esi": 3,
                "confidence": 0.5,
                "reason": f"Classification error: {exc}",
                "flags": [],
                "severity_score": 0.0,
                "has_red_flags": False,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "cost_usd": 0.0,
            }
