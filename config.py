import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./quizella.db"
    )

    SECRET_KEY = os.getenv("SECRET_KEY")

    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            "30"
        )
    )

    # Admin panel credentials are intentionally kept outside the source code.
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    # Comma-separated list:
    # CORS_ORIGINS=http://localhost:3000,http://localhost:5173
    _cors_origins = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:5173"
    )

    CORS_ORIGINS = [
        origin.strip()
        for origin in _cors_origins.split(",")
        if origin.strip()
    ]

    # Hosts used by local development and the Android emulator.
    _allowed_hosts = os.getenv(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1,10.0.2.2"
    )

    ALLOWED_HOSTS = [
        host.strip()
        for host in _allowed_hosts.split(",")
        if host.strip()
    ]


settings = Settings()


if not settings.SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not configured. "
        "Set a strong SECRET_KEY environment variable."
    )

if len(settings.SECRET_KEY) < 32:
    raise RuntimeError(
        "SECRET_KEY must be at least 32 characters long."
    )

if not settings.ADMIN_USERNAME or not settings.ADMIN_PASSWORD:
    raise RuntimeError(
        "ADMIN_USERNAME and ADMIN_PASSWORD must be configured."
    )

if len(settings.ADMIN_PASSWORD) < 12:
    raise RuntimeError(
        "ADMIN_PASSWORD must be at least 12 characters long."
    )

if settings.ACCESS_TOKEN_EXPIRE_MINUTES < 5:
    raise RuntimeError(
        "ACCESS_TOKEN_EXPIRE_MINUTES must be at least 5 minutes."
    )