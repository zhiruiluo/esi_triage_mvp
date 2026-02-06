import re
from typing import Any, Dict, Optional

from config import settings
from rag.config import RAGConfigManager
from rag.knowledge_base import KnowledgeBase


class VitalSignalDetector:
    def __init__(self) -> None:
        self.rag_config = RAGConfigManager()

    def _extract_age(self, text: str) -> Optional[int]:
        match = re.search(r"(\d{1,3})\s*(?:years?|yo|y/o|yr)\b", text.lower())
        if match:
            return int(match.group(1))
        return None

    def _extract_vitals(self, text: str) -> Dict[str, Any]:
        vitals: Dict[str, Any] = {}
        text_lower = text.lower()

        hr = re.search(r"\bhr\s*(\d{2,3})\b", text_lower)
        if hr:
            vitals["hr"] = int(hr.group(1))

        rr = re.search(r"\brr\s*(\d{1,2})\b", text_lower)
        if rr:
            vitals["rr"] = int(rr.group(1))

        bp = re.search(r"\bbp\s*(\d{2,3})\s*/\s*(\d{2,3})\b", text_lower)
        if bp:
            vitals["sbp"] = int(bp.group(1))
            vitals["dbp"] = int(bp.group(2))

        temp = re.search(r"\b(?:t|temp|temperature)\s*([0-9]{2,3}(?:\.[0-9])?)", text_lower)
        if temp:
            vitals["temp_f"] = float(temp.group(1))

        spo2 = re.search(r"\b(?:spo2|o2\s*sat)\s*(\d{2,3})%", text_lower)
        if spo2:
            vitals["spo2"] = int(spo2.group(1))

        return vitals

    def _parse_range(self, value: str) -> Dict[str, Optional[float]]:
        numbers = [float(n) for n in re.findall(r"\d+\.?\d*", value)]
        if "<" in value and numbers:
            return {"min": None, "max": numbers[0]}
        if "up to" in value.lower() and numbers:
            return {"min": None, "max": numbers[0]}
        if len(numbers) >= 2:
            return {"min": numbers[0], "max": numbers[1]}
        if len(numbers) == 1:
            return {"min": numbers[0], "max": numbers[0]}
        return {"min": None, "max": None}

    def _is_out_of_range(self, value: Optional[float], range_str: str) -> Optional[bool]:
        if value is None:
            return None
        parsed = self._parse_range(range_str)
        min_val = parsed.get("min")
        max_val = parsed.get("max")
        if min_val is not None and value < min_val:
            return True
        if max_val is not None and value > max_val:
            return True
        return False

    async def assess(self, case_text: str) -> Dict[str, Any]:
        age = self._extract_age(case_text)
        vitals = self._extract_vitals(case_text)

        layer_config = self.rag_config.get_layer_config(4)
        rag_enabled = bool(
            layer_config
            and self.rag_config.config.global_settings.get("enable_rag_globally")
            and layer_config.enabled
        )

        evidence = None
        if rag_enabled and age is not None:
            kb = KnowledgeBase(
                {
                    "openrouter_api_key": settings.OPENROUTER_API_KEY,
                    "openrouter_base_url": settings.OPENROUTER_BASE_URL,
                    "use_vector_db": layer_config.use_vector_db,
                }
            )
            retrieval = await kb.retrieve_vital_norms(age)
            evidence = retrieval.results[0] if retrieval.results else None

        abnormalities = {}
        if evidence:
            abnormalities["hr"] = self._is_out_of_range(vitals.get("hr"), evidence.get("hr_normal", ""))
            abnormalities["rr"] = self._is_out_of_range(vitals.get("rr"), evidence.get("rr_normal", ""))
            abnormalities["sbp"] = self._is_out_of_range(vitals.get("sbp"), evidence.get("sbp_normal", ""))
            abnormalities["temp_f"] = self._is_out_of_range(vitals.get("temp_f"), evidence.get("temp_normal", ""))

        # Basic severity flags
        critical = False
        if vitals.get("spo2") is not None and vitals["spo2"] < 90:
            critical = True
        if vitals.get("sbp") is not None and vitals["sbp"] < 90:
            critical = True
        if vitals.get("rr") is not None and vitals["rr"] >= 30:
            critical = True

        return {
            "age": age,
            "vitals": vitals,
            "abnormalities": abnormalities,
            "critical": critical,
            "rag": {
                "enabled": rag_enabled,
                "evidence": evidence,
            },
        }
