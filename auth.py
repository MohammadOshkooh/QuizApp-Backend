import bcrypt

from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe
from typing import Any

from jose import jwt

from config import settings


def hash_password(password: str) -> str:
    """
    Hash a user's password using bcrypt.

    bcrypt has a maximum password size of 72 bytes.
    """

    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        raise ValueError(
            "Password cannot be longer than 72 bytes."
        )

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(
        password_bytes,
        salt
    )

    return hashed.decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify a plaintext password against a bcrypt hash.
    """

    try:
        password_bytes = plain_password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")

        if len(password_bytes) > 72:
            return False

        return bcrypt.checkpw(
            password_bytes,
            hashed_bytes
        )

    except (
        ValueError,
        TypeError,
        bcrypt.errors.InvalidHashError
    ):
        return False


def create_access_token(
    user_id: int,
    expires_delta: timedelta | None = None
) -> str:
    """
    Create a JWT access token.

    The user's database ID is stored in `sub`. A unique JTI is included so
    tokens can be identified if token revocation is added later.
    """

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    now = datetime.now(timezone.utc)
    expire = now + expires_delta

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "type": "access",
        "jti": token_urlsafe(16),
        "iat": now,
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )