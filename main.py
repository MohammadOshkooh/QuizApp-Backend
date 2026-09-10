import base64
import binascii
import sys
from pathlib import Path
from secrets import compare_digest

sys.path.append(
    str(Path(__file__).parent)
)

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from config import settings
from database import (
    Base,
    engine,
    migrate_schema
)

from routers import (
    auth,
    categories,
    questions,
    results,
    users
)

from admin import setup_admin


# Database initialization

migrate_schema()

Base.metadata.create_all(
    bind=engine
)


# Application

app = FastAPI(
    title="QuizeApp API",
    version="1.3.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Reject requests with unexpected Host headers.

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)


# CORS

app.add_middleware(
    CORSMiddleware,

    allow_origins=settings.CORS_ORIGINS,

    # Authentication uses Authorization: Bearer rather than cookies.
    # Credentials are therefore not needed and are safer disabled.
    allow_credentials=False,

    allow_methods=[
        "GET",
        "POST",
        "OPTIONS"
    ],

    allow_headers=[
        "Authorization",
        "Content-Type",
        "Accept"
    ]
)


# Admin panel protection.
# SQLAdmin itself does not automatically protect the panel. Basic Auth keeps
# the existing admin UI intact while preventing anonymous access.

@app.middleware("http")
async def protect_admin_panel(
    request: Request,
    call_next
):
    if (
        request.url.path == "/admin"
        or request.url.path.startswith("/admin/")
    ):
        authorization = request.headers.get(
            "Authorization",
            ""
        )

        if not authorization.startswith("Basic "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Admin authentication required."
                },
                headers={
                    "WWW-Authenticate":
                        'Basic realm="Quizella Admin"'
                }
            )

        try:
            encoded_credentials = (
                authorization[6:].strip()
            )

            decoded_credentials = (
                base64.b64decode(
                    encoded_credentials,
                    validate=True
                )
                .decode("utf-8")
            )

            username, password = (
                decoded_credentials.split(
                    ":",
                    1
                )
            )

        except (
            ValueError,
            UnicodeDecodeError,
            binascii.Error
        ):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Invalid admin credentials."
                },
                headers={
                    "WWW-Authenticate":
                        'Basic realm="Quizella Admin"'
                }
            )

        if not (
            compare_digest(
                username,
                settings.ADMIN_USERNAME
            )
            and compare_digest(
                password,
                settings.ADMIN_PASSWORD
            )
        ):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Invalid admin credentials."
                },
                headers={
                    "WWW-Authenticate":
                        'Basic realm="Quizella Admin"'
                }
            )

    return await call_next(request)


# Security headers

@app.middleware("http")
async def add_security_headers(
    request,
    call_next
):
    response = await call_next(request)

    response.headers[
        "X-Content-Type-Options"
    ] = "nosniff"

    response.headers[
        "X-Frame-Options"
    ] = "DENY"

    response.headers[
        "Referrer-Policy"
    ] = "strict-origin-when-cross-origin"

    response.headers[
        "Permissions-Policy"
    ] = (
        "camera=(), "
        "microphone=(), "
        "geolocation=()"
    )

    # Only advertise HTTPS when the request is actually HTTPS. This avoids
    # breaking the local HTTP setup used by the Android emulator.
    if request.url.scheme == "https":
        response.headers[
            "Strict-Transport-Security"
        ] = (
            "max-age=31536000; "
            "includeSubDomains"
        )

    # Authentication responses should never be cached by browsers/proxies.
    if request.url.path.startswith(
        "/api/auth/"
    ):
        response.headers[
            "Cache-Control"
        ] = "no-store"

    return response


# Static media

MEDIA_DIR = Path(__file__).parent / "media"

MEDIA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

app.mount(
    "/media",
    StaticFiles(
        directory=str(MEDIA_DIR)
    ),
    name="media"
)


# Routers

app.include_router(
    auth.router
)

app.include_router(
    questions.router
)

app.include_router(
    users.router
)

app.include_router(
    categories.router
)

app.include_router(
    results.router
)


# Admin

setup_admin(app)


# Basic endpoints

@app.get("/")
def root():
    return {
        "message": "QuizeApp API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }