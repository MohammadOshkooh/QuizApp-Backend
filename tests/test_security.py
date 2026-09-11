import pytest

from fastapi import HTTPException
from starlette.requests import Request

from security import (
    RateLimiter,
    get_client_ip,
)

from .conftest import client


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "QuizeApp API is running"
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok"
    }


def test_security_headers():
    response = client.get("/health")

    assert response.headers["X-Content-Type-Options"] == "nosniff"

    assert response.headers["X-Frame-Options"] == "DENY"

    assert response.headers["Referrer-Policy"] == (
        "strict-origin-when-cross-origin"
    )

    assert response.headers["Permissions-Policy"] == (
        "camera=(), "
        "microphone=(), "
        "geolocation=()"
    )


def test_auth_responses_are_not_cached():
    response = client.post(
        "/api/auth/login",
        json={
            "username": "unknown",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401

    assert response.headers["Cache-Control"] == "no-store"


def test_cors():
    response = client.options(
        "/api/auth/login",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200

    assert response.headers.get(
        "access-control-allow-origin"
    ) == "http://localhost:3000"


def test_https_gets_hsts_header():
    https_client = client.__class__(
        client.app,
        base_url="https://testserver",
    )

    response = https_client.get("/health")

    assert response.status_code == 200

    assert response.headers["Strict-Transport-Security"] == (
        "max-age=31536000; includeSubDomains"
    )


def test_http_does_not_get_hsts_header():
    http_client = client.__class__(
        client.app,
        base_url="http://testserver",
    )

    response = http_client.get("/health")

    assert response.status_code == 200

    assert "Strict-Transport-Security" not in response.headers


def test_rate_limiter():
    limiter = RateLimiter(
        max_requests=2,
        window_seconds=60,
    )

    limiter.check("client")
    limiter.check("client")

    with pytest.raises(HTTPException) as exc:
        limiter.check("client")

    assert exc.value.status_code == 429

    assert exc.value.detail == (
        "Too many requests. Please try again later."
    )

    assert exc.value.headers["Retry-After"] == "60"


def test_rate_limiter_is_separate_per_key():
    limiter = RateLimiter(
        max_requests=1,
        window_seconds=60,
    )

    limiter.check("user-1")
    limiter.check("user-2")

    with pytest.raises(HTTPException):
        limiter.check("user-1")

    # user-2 should still have its own quota.
    limiter.check("user-3")


def test_get_client_ip():
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/health",
        "query_string": b"",
        "headers": [],
        "client": ("127.0.0.1", 8000),
        "server": ("testserver", 80),
        "scheme": "http",
    }

    request = Request(scope)

    ip = get_client_ip(request)

    assert ip is not None
    assert isinstance(ip, str)
    assert ip == "127.0.0.1"

