from typing import Any, Dict, List

from config import settings
from rag.config import RAGConfigManager
from rag.knowledge_base import KnowledgeBase


class ResourceInferenceDetector:
    def __init__(self) -> None:
        self.rag_config = RAGConfigManager()

    def _infer_resources(self, text: str) -> List[str]:
        text_lower = text.lower()
        resources: List[str] = []

        if "chest pain" in text_lower or "chest" in text_lower:
            resources.extend(["ECG", "Troponin", "CXR"])

        if "shortness of breath" in text_lower or "sob" in text_lower or "dyspnea" in text_lower:
            resources.extend(["CXR", "CBC"])

        if "fever" in text_lower or "sepsis" in text_lower or "infection" in text_lower:
            resources.extend(["CBC", "Lactate"])

        if "laceration" in text_lower or "wound" in text_lower:
            resources.append("Sutures")

        if "fracture" in text_lower or "wrist" in text_lower or "arm" in text_lower:
            resources.append("X-ray")

        if "abdominal pain" in text_lower:
            resources.extend(["CBC", "CMP", "CT Abdomen"])

        # Deduplicate while preserving order
        seen = set()
        deduped = []
        for res in resources:
            if res not in seen:
                seen.add(res)
                deduped.append(res)
        return deduped

    async def infer(self, case_text: str, extracted: Dict[str, Any] = None) -> Dict[str, Any]:
        text = case_text
        if extracted:
            keywords = extracted.get("keywords", [])
            if keywords:
                text = " ".join(keywords)
        resources = self._infer_resources(text)
        resource_count = len(resources)

        layer_config = self.rag_config.get_layer_config(5)
        rag_enabled = bool(
            layer_config
            and self.rag_config.config.global_settings.get("enable_rag_globally")
            and layer_config.enabled
        )

        evidence: List[Dict[str, Any]] = []
        if rag_enabled:
            kb = KnowledgeBase(
                {
                    "openrouter_api_key": settings.OPENROUTER_API_KEY,
                    "openrouter_base_url": settings.OPENROUTER_BASE_URL,
                    "use_vector_db": layer_config.use_vector_db,
                }
            )
            for test in resources:
                if test in {"Troponin", "CBC", "Lactate", "D-dimer", "Procalcitonin"}:
                    retrieval = await kb.retrieve_lab_indications(test)
                    if retrieval.results:
                        evidence.extend(retrieval.results[:1])

        return {
            "resources": resources,
            "resource_count": resource_count,
            "rag": {
                "enabled": rag_enabled,
                "evidence": evidence,
            },
        }
