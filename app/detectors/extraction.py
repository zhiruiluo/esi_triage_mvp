import re
from typing import Any, Dict, List, Optional


class ExtractionDetector:
    def __init__(self) -> None:
        pass

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

    def _extract_chief_complaint(self, text: str) -> str:
        text_lower = text.lower()
        if "chest pain" in text_lower or "chest pressure" in text_lower:
            return "Chest Pain"
        if "shortness of breath" in text_lower or "sob" in text_lower or "dyspnea" in text_lower:
            return "Shortness of Breath"
        if "altered mental" in text_lower or "ams" in text_lower or "confus" in text_lower:
            return "Altered Mental Status"
        if "abdominal pain" in text_lower:
            return "Abdominal Pain"
        if "fever" in text_lower:
            return "Fever"
        return "General"

    def _extract_keywords(self, text: str) -> List[str]:
        keywords = []
        text_lower = text.lower()
        for term in [
            "chest pain",
            "shortness of breath",
            "sob",
            "dyspnea",
            "fever",
            "sepsis",
            "infection",
            "laceration",
            "wound",
            "fracture",
            "wrist",
            "arm",
            "abdominal pain",
            "trauma",
        ]:
            if term in text_lower:
                keywords.append(term)
        return keywords

    def extract(self, case_text: str) -> Dict[str, Any]:
        return {
            "age": self._extract_age(case_text),
            "vitals": self._extract_vitals(case_text),
            "chief_complaint": self._extract_chief_complaint(case_text),
            "keywords": self._extract_keywords(case_text),
            "raw_text": case_text,
        }
