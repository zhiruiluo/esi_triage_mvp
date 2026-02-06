from typing import Any, Dict

from config import settings
from rag.config import RAGConfigManager
from rag.knowledge_base import KnowledgeBase


class HandbookVerificationDetector:
    def __init__(self) -> None:
        self.rag_config = RAGConfigManager()

    async def verify(self, esi_level: int, case_text: str) -> Dict[str, Any]:
        layer_config = self.rag_config.get_layer_config(6)
        rag_enabled = bool(
            layer_config
            and self.rag_config.config.global_settings.get("enable_rag_globally")
            and layer_config.enabled
        )

        evidence = None
        if rag_enabled:
            kb = KnowledgeBase(
                {
                    "openrouter_api_key": settings.OPENROUTER_API_KEY,
                    "openrouter_base_url": settings.OPENROUTER_BASE_URL,
                    "use_vector_db": layer_config.use_vector_db,
                }
            )
            retrieval = await kb.retrieve_esi_criteria(esi_level)
            evidence = retrieval.results[0] if retrieval.results else None

        confidence = 0.85 if evidence else 0.5
        return {
            "esi_level": esi_level,
            "confidence": confidence,
            "rag": {
                "enabled": rag_enabled,
                "evidence": evidence,
            },
        }
