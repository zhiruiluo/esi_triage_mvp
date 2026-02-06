import re
from typing import Dict, List


INJECTION_PATTERNS = [
    r"ignore (all|any) (previous|prior) instructions",
    r"system override",
    r"reveal (your|the) system prompt",
    r"show (your|the) system prompt",
    r"disclose (your|the) system prompt",
    r"jailbreak",
    r"do anything now",
    r"developer message",
    r"act as",
    r"bypass",
]

SUSPICIOUS_MARKERS = [
    "SYSTEM OVERRIDE",
    "IGNORE ALL PREVIOUS INSTRUCTIONS",
    "REVEAL YOUR SYSTEM PROMPT",
]


class MaliciousInputDetector:
    def __init__(self) -> None:
        self._compiled = [re.compile(pat, re.IGNORECASE) for pat in INJECTION_PATTERNS]

    def analyze(self, text: str) -> Dict[str, object]:
        matches: List[str] = []
        for pattern in self._compiled:
            if pattern.search(text):
                matches.append(pattern.pattern)

        markers_found = [marker for marker in SUSPICIOUS_MARKERS if marker in text]
        is_malicious = bool(matches or markers_found)

        sanitized_text = text
        if is_malicious:
            sanitized_text = self._sanitize(text)

        return {
            "is_malicious": is_malicious,
            "pattern_matches": matches,
            "markers": markers_found,
            "sanitized_text": sanitized_text,
        }

    def _sanitize(self, text: str) -> str:
        lines = []
        for line in text.splitlines():
            if any(marker in line for marker in SUSPICIOUS_MARKERS):
                continue
            if any(pattern.search(line) for pattern in self._compiled):
                continue
            lines.append(line)
        return "\n".join(lines).strip()
