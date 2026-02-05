"""Admin authentication middleware."""
from fastapi import Header, HTTPException
from config import settings


def verify_admin_key(x_admin_key: str = Header(None)):
    """Verify admin API key from header."""
    admin_key = getattr(settings, "ADMIN_API_KEY", "admin123")  # Default for MVP
    
    if not x_admin_key:
        raise HTTPException(
            status_code=401,
            detail="Admin API key required. Include X-Admin-Key header."
        )
    
    if x_admin_key != admin_key:
        raise HTTPException(
            status_code=403,
            detail="Invalid admin API key"
        )
    
    return True
