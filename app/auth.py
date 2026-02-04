from datetime import datetime
from typing import Dict

from config import settings


class RateLimiter:
    def __init__(self) -> None:
        self.limits: Dict[str, int] = {}
        self.daily_limit = settings.RATE_LIMIT_PER_DAY

    def _key(self, ip: str) -> str:
        today = datetime.now().strftime("%Y-%m-%d")
        return f"{ip}:{today}"

    def check_limit(self, ip: str) -> tuple[bool, str]:
        key = self._key(ip)
        count = self.limits.get(key, 0)
        if count >= self.daily_limit:
            return False, f"Rate limit exceeded ({self.daily_limit} per day)"
        return True, "OK"

    def increment(self, ip: str) -> None:
        key = self._key(ip)
        self.limits[key] = self.limits.get(key, 0) + 1

    def get_remaining(self, ip: str) -> int:
        key = self._key(ip)
        count = self.limits.get(key, 0)
        return max(0, self.daily_limit - count)
