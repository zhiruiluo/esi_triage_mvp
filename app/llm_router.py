from typing import Any, Dict, Optional

from config import settings


class LLMRouter:
    """Route requests to different LLM models based on risk and uncertainty."""

    HIGH_RISK_TERMS = {
        "chest pain",
        "chest pressure",
        "shortness of breath",
        "sob",
        "dyspnea",
        "stroke",
        "cva",
        "seizure",
        "unresponsive",
        "altered mental",
        "ams",
        "confus",
        "anaphylaxis",
        "severe bleeding",
        "hemorrhage",
        "trauma",
        "shock",
        "hypotension",
        "hypoxia",
    }

    def _contains_high_risk_terms(self, text: str, extracted: Optional[Dict[str, Any]] = None) -> bool:
        text_lower = text.lower()
        if any(term in text_lower for term in self.HIGH_RISK_TERMS):
            return True
        if extracted:
            keywords = extracted.get("keywords", [])
            if any(term in " ".join(keywords).lower() for term in self.HIGH_RISK_TERMS):
                return True
            chief = extracted.get("chief_complaint", "").lower()
            if any(term in chief for term in self.HIGH_RISK_TERMS):
                return True
        return False

    def _vitals_critical(self, vitals: Optional[Dict[str, Any]]) -> bool:
        if not vitals:
            return False
        spo2 = vitals.get("spo2")
        sbp = vitals.get("sbp")
        rr = vitals.get("rr")
        hr = vitals.get("hr")
        temp_f = vitals.get("temp_f")
        return bool(
            (spo2 is not None and spo2 < 90)
            or (sbp is not None and sbp < 90)
            or (rr is not None and rr >= 30)
            or (hr is not None and hr >= 130)
            or (temp_f is not None and temp_f >= 104)
        )

    def select_red_flag_model(self, case_text: str, extracted: Optional[Dict[str, Any]] = None) -> str:
        if not settings.ROUTER_ENABLED:
            return settings.LLM_MODEL

        vitals = extracted.get("vitals") if extracted else None
        if self._contains_high_risk_terms(case_text, extracted) or self._vitals_critical(vitals):
            return settings.ROUTER_HIGH_MODEL

        return settings.ROUTER_DEFAULT_MODEL

    def select_final_decision_model(self, case_text: str, context: Dict[str, Any]) -> str:
        if not settings.ROUTER_ENABLED:
            return settings.LLM_MODEL

        esi_level = context.get("esi_level", 3)
        red_flags = context.get("red_flags", {})
        vitals = context.get("vitals", {})
        resources = context.get("resources", {})
        handbook = context.get("handbook_verification", {})
        extracted = context.get("extraction", {})

        if esi_level <= 2 or vitals.get("critical") or red_flags.get("has_red_flags"):
            return settings.ROUTER_HIGH_MODEL

        low_conf = settings.ROUTER_LOW_CONFIDENCE_THRESHOLD
        if red_flags.get("confidence", 1.0) < low_conf:
            return settings.ROUTER_MID_MODEL
        if handbook.get("confidence", 1.0) < low_conf:
            return settings.ROUTER_MID_MODEL

        if resources.get("resource_count", 0) >= settings.ROUTER_RESOURCE_COUNT_FOR_MID and esi_level >= 3:
            return settings.ROUTER_MID_MODEL

        if self._contains_high_risk_terms(case_text, extracted):
            return settings.ROUTER_MID_MODEL

        return settings.ROUTER_DEFAULT_MODEL
