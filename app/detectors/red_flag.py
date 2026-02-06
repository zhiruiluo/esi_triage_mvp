import json
from typing import Any, Dict, List

from openai import AsyncOpenAI

from config import settings
from rag.config import RAGConfigManager
from rag.knowledge_base import KnowledgeBase, RetrievalResult


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
        self.rag_config = RAGConfigManager()

    def _extract_chief_complaint(self, case_text: str) -> str:
        text = case_text.lower()
        if "chest pain" in text or "chestpressure" in text:
            return "Chest Pain"
        if "shortness of breath" in text or "sob" in text or "dyspnea" in text:
            return "Shortness of Breath"
        if "altered mental" in text or "ams" in text or "confus" in text:
            return "Altered Mental Status"
        return "General"

    async def _build_rag_context(self, case_text: str, extracted: Dict[str, Any] = None) -> Dict[str, Any]:
        layer_config = self.rag_config.get_layer_config(3)
        if not layer_config:
            return {"enabled": False, "context": "", "sources": [], "queries": []}

        if not self.rag_config.config.global_settings.get("enable_rag_globally"):
            return {"enabled": False, "context": "", "sources": [], "queries": []}

        if not layer_config.enabled:
            return {"enabled": False, "context": "", "sources": [], "queries": []}

        kb = KnowledgeBase(
            {
                "openrouter_api_key": settings.OPENROUTER_API_KEY,
                "openrouter_base_url": settings.OPENROUTER_BASE_URL,
                "use_vector_db": layer_config.use_vector_db,
            }
        )

        chief_complaint = extracted.get("chief_complaint") if extracted else self._extract_chief_complaint(case_text)
        retrievals: List[RetrievalResult] = []

        if "esi_handbook" in layer_config.knowledge_sources:
            retrievals.append(await kb.retrieve_esi_criteria(2, chief_complaint))

        if "differential_diagnosis" in layer_config.knowledge_sources:
            retrievals.append(await kb.retrieve_differential_diagnoses(chief_complaint))

        if "acs_protocols" in layer_config.knowledge_sources and "chest" in case_text.lower():
            retrievals.append(await kb.retrieve_acs_protocols(chief_complaint))

        if "sepsis_criteria" in layer_config.knowledge_sources and "fever" in case_text.lower():
            retrievals.append(await kb.retrieve_sepsis_criteria(chief_complaint))

        context_blocks: List[str] = []
        for item in retrievals:
            context_blocks.append(await kb.format_for_llm(item))

        return {
            "enabled": True,
            "context": "\n".join(context_blocks),
            "sources": [item.collection for item in retrievals],
            "queries": [item.query for item in retrievals],
            "num_results": sum(item.num_results for item in retrievals),
        }

    async def classify(self, case_text: str, extracted: Dict[str, Any] = None) -> Dict[str, Any]:
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
            rag_info = await self._build_rag_context(case_text, extracted)
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
            ]

            if rag_info["enabled"] and rag_info["context"]:
                messages.append(
                    {
                        "role": "system",
                        "content": f"Use the following clinical evidence to support your decision:\n{rag_info['context']}",
                    }
                )

            messages.append({"role": "user", "content": f"Case: {case_text}"})

            response = await self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=messages,
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
                "rag": {
                    "enabled": rag_info.get("enabled", False),
                    "sources": rag_info.get("sources", []),
                    "queries": rag_info.get("queries", []),
                    "num_results": rag_info.get("num_results", 0),
                },
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
                "rag": {
                    "enabled": False,
                    "sources": [],
                    "queries": [],
                    "num_results": 0,
                },
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "cost_usd": 0.0,
            }
