from datetime import datetime
from typing import Dict

from config import settings


class RateLimiter:
    def __init__(self) -> None:
        self.limits: Dict[str, int] = {}
        self.costs: Dict[str, float] = {}
        self.daily_limit = settings.RATE_LIMIT_PER_DAY
        self.daily_budget = settings.FREE_TIER_DAILY_BUDGET_USD

    def _key(self, ip: str) -> str:
        today = datetime.now().strftime("%Y-%m-%d")
        return f"{ip}:{today}"

    def check_limit(self, ip: str) -> tuple[bool, str]:
        key = self._key(ip)
        count = self.limits.get(key, 0)
        if count >= self.daily_limit:
            return False, f"Rate limit exceeded ({self.daily_limit} per day)"
        if self.daily_budget > 0:
            spent = self.costs.get(key, 0.0)
            if spent >= self.daily_budget:
                return False, f"Free-tier budget exceeded (${self.daily_budget:.2f} per day)"
        return True, "OK"

    def increment(self, ip: str) -> None:
        key = self._key(ip)
        self.limits[key] = self.limits.get(key, 0) + 1

    def get_remaining(self, ip: str) -> int:
        key = self._key(ip)
        count = self.limits.get(key, 0)
        return max(0, self.daily_limit - count)

    def add_cost(self, ip: str, amount: float) -> None:
        key = self._key(ip)
        self.costs[key] = self.costs.get(key, 0.0) + max(0.0, amount)

    def get_remaining_budget(self, ip: str) -> float:
        if self.daily_budget <= 0:
            return float("inf")
        key = self._key(ip)
        spent = self.costs.get(key, 0.0)
        return max(0.0, self.daily_budget - spent)
