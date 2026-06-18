import logging
import time
from collections import defaultdict
from typing import Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.config import API_KEY, API_KEY_ENABLED, CORS_ORIGINS, RATE_LIMIT_PER_MINUTE

logger = logging.getLogger(__name__)

# ─── API Key Auth ────────────────────────────────────────────────────────────


class AuthMiddleware(BaseHTTPMiddleware):
    """Require API key on all endpoints except health check and docs."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not API_KEY_ENABLED:
            return await call_next(request)

        path = request.url.path
        method = request.method
        # Allow unauthenticated access to health, docs, openapi, and CORS preflight
        if method == "OPTIONS" or path in ("/", "/health", "/docs", "/openapi.json", "/redoc"):
            return await call_next(request)

        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer ") and auth_header[len("Bearer "):] == API_KEY:
            return await call_next(request)

        return JSONResponse(
            status_code=401,
            content={"detail": "Missing or invalid API key. Provide Authorization: Bearer <key>"},
        )

# ─── Rate Limiting ───────────────────────────────────────────────────────────

_rate_store: dict[str, list[float]] = defaultdict(list)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple fixed-window rate limiter per IP."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window = 60.0

        timestamps = _rate_store[client_ip]
        cutoff = now - window
        # Keep only timestamps within the window
        timestamps[:] = [t for t in timestamps if t > cutoff]

        if len(timestamps) >= RATE_LIMIT_PER_MINUTE:
            logger.warning("Rate limit exceeded for %s (%d/min)", client_ip, RATE_LIMIT_PER_MINUTE)
            return JSONResponse(
                status_code=429,
                content={"detail": f"Rate limit exceeded. Max {RATE_LIMIT_PER_MINUTE} requests per minute."},
                headers={"Retry-After": str(int(window))},
            )

        timestamps.append(now)
        return await call_next(request)


# ─── Security Headers (HSTS, etc.) ──────────────────────────────────────────


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Cache-Control"] = "no-store"
        return response


# ─── Middleware Registration ────────────────────────────────────────────────


def register_middleware(app: FastAPI) -> None:
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(AuthMiddleware)
    app.add_middleware(RateLimitMiddleware)
    logger.info(
        "Middleware registered: auth=%s, rate_limit=%d/min, cors_origins=%s",
        API_KEY_ENABLED,
        RATE_LIMIT_PER_MINUTE,
        CORS_ORIGINS,
    )
