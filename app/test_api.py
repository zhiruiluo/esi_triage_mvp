"""
Comprehensive API tests for ESI Triage Classifier
Tests endpoints, rate limiting, error handling, and edge cases
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_info_endpoint():
    """Test API info endpoint"""
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data or "title" in data
    assert "version" in data


def test_classify_missing_case_text():
    """Test classify with missing case_text field"""
    response = client.post("/classify", json={})
    assert response.status_code == 422  # Validation error


def test_classify_empty_case_text():
    """Test classify with empty case_text"""
    response = client.post("/classify", json={"case_text": ""})
    assert response.status_code == 422  # Should require non-empty text


def test_classify_valid_case_no_api_key():
    """Test classify with valid input but no API key"""
    # Clear API key temporarily
    from config import settings
    original_key = settings.OPENROUTER_API_KEY
    settings.OPENROUTER_API_KEY = None
    
    response = client.post("/classify", json={
        "case_text": "Patient with minor abrasion"
    })
    
    # Should return error response
    assert response.status_code in [200, 500]
    data = response.json()
    
    # Restore API key
    settings.OPENROUTER_API_KEY = original_key
    
    # Check response structure
    if response.status_code == 200:
        assert "esi_level" in data or "error" in data


def test_rate_limiting_logic():
    """Test rate limiting functionality"""
    from auth import RateLimiter
    from config import settings
    
    # Create temporary limiter with modified settings
    original_limit = settings.RATE_LIMIT_PER_DAY
    settings.RATE_LIMIT_PER_DAY = 3
    limiter = RateLimiter()
    test_ip = "192.168.1.100"
    
    # First 3 requests should pass
    for i in range(3):
        allowed, _ = limiter.check_limit(test_ip)
        assert allowed, f"Request {i+1} should be allowed"
        limiter.increment(test_ip)
    
    # 4th request should be blocked
    allowed, msg = limiter.check_limit(test_ip)
    assert not allowed, "Request beyond limit should be blocked"
    assert "Rate limit exceeded" in msg
    
    # Restore original limit
    settings.RATE_LIMIT_PER_DAY = original_limit


def test_classify_response_structure():
    """Test that classify response has required fields"""
    response = client.post("/classify", json={
        "case_text": "Patient presents with minor cut on finger, no bleeding"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields
    assert "esi_level" in data
    assert "confidence" in data
    assert "reason" in data
    assert "queries_remaining" in data


def test_classify_invalid_method():
    """Test classify with GET instead of POST"""
    response = client.get("/classify")
    assert response.status_code == 405  # Method not allowed


def test_classify_malformed_json():
    """Test classify with malformed JSON"""
    from fastapi.testclient import TestClient
    response = client.post(
        "/classify",
        data="not json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422


if __name__ == "__main__":
    print("Running comprehensive API tests...\n")
    
    tests = [
        test_health_endpoint,
        test_info_endpoint,
        test_classify_missing_case_text,
        test_classify_empty_case_text,
        test_classify_valid_case_no_api_key,
        test_rate_limiting_logic,
        test_classify_response_structure,
        test_classify_invalid_method,
        test_classify_malformed_json,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"✓ {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: Unexpected error - {e}")
            failed += 1
    
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
