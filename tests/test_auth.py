import pytest

from auth import (
    hash_password,
    verify_password,
)
from config import settings
from jose import jwt

from .conftest import client


def test_register_success():
    response = client.post(
        "/api/auth/register",
        json={
            "username": "john123",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["username"] == "john123"
    assert "created_at" in data

    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_username():
    first = client.post(
        "/api/auth/register",
        json={
            "username": "sameuser",
            "password": "password123",
        },
    )

    assert first.status_code == 201

    second = client.post(
        "/api/auth/register",
        json={
            "username": "sameuser",
            "password": "password123",
        },
    )

    assert second.status_code == 409
    assert (
        second.json()["detail"]
        == "Username already exists."
    )


@pytest.mark.parametrize(
    "username",
    [
        "ab",
        "invalid username",
        "invalid@username",
    ],
)
def test_register_invalid_username(username):
    response = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "password": "password123",
        },
    )

    assert response.status_code == 422


def test_register_short_password():
    response = client.post(
        "/api/auth/register",
        json={
            "username": "john123",
            "password": "1234567",
        },
    )

    assert response.status_code == 422


def test_register_password_over_72_bytes():
    response = client.post(
        "/api/auth/register",
        json={
            "username": "john123",
            "password": "a" * 73,
        },
    )

    assert response.status_code == 422


def test_register_multibyte_password_over_limit():
    password = "آ" * 40

    assert len(password.encode("utf-8")) > 72

    response = client.post(
        "/api/auth/register",
        json={
            "username": "persianuser",
            "password": password,
        },
    )

    assert response.status_code == 422


def test_login_success():
    client.post(
        "/api/auth/register",
        json={
            "username": "loginuser",
            "password": "password123",
        },
    )

    response = client.post(
        "/api/auth/login",
        json={
            "username": "loginuser",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    client.post(
        "/api/auth/register",
        json={
            "username": "loginuser",
            "password": "password123",
        },
    )

    response = client.post(
        "/api/auth/login",
        json={
            "username": "loginuser",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == (
        "Invalid credentials."
    )


def test_login_unknown_user():
    response = client.post(
        "/api/auth/login",
        json={
            "username": "doesnotexist",
            "password": "password123",
        },
    )

    assert response.status_code == 401


def test_password_hash_and_verify():
    password = "password123"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(
        password,
        hashed,
    )

    assert not verify_password(
        "wrongpassword",
        hashed,
    )


def test_access_token_claims():
    from auth import create_access_token

    token = create_access_token(42)

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    assert payload["sub"] == "42"
    assert payload["type"] == "access"
    assert "jti" in payload
    assert "iat" in payload
    assert "exp" in payload