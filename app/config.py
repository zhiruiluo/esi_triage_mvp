import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    API_TITLE = "ESI Triage Classifier - MVP"
    API_VERSION = "1.0.0-mvp"

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4-turbo")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "300"))

    RATE_LIMIT_PER_DAY = int(os.getenv("RATE_LIMIT_PER_DAY", "20"))
    FREE_TIER_DAILY_BUDGET_USD = float(os.getenv("FREE_TIER_DAILY_BUDGET_USD", "1.00"))
    COST_PER_1K_INPUT = float(os.getenv("COST_PER_1K_INPUT", "0.01"))
    COST_PER_1K_OUTPUT = float(os.getenv("COST_PER_1K_OUTPUT", "0.03"))
    
    # Admin authentication
    ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "admin123")


settings = Settings()
