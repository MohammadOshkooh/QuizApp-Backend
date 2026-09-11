from .conftest import client


def test_get_me(auth_headers):
    response = client.get(
        "/api/users/me",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "testuser"
    assert "id" in data
    assert "created_at" in data

    assert "password" not in data
    assert "hashed_password" not in data


def test_get_me_without_authentication():
    response = client.get(
        "/api/users/me"
    )

    assert response.status_code == 401


def test_get_me_with_invalid_token():
    response = client.get(
        "/api/users/me",
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401


def test_get_me_with_non_access_token(
    db,
    registered_user,
):
    from datetime import datetime, timedelta, timezone

    from config import settings
    from jose import jwt

    token = jwt.encode(
        {
            "sub": str(registered_user["id"]),
            "type": "quiz",
            "jti": "test-jti",
            "iat": datetime.now(timezone.utc),
            "exp": (
                datetime.now(timezone.utc)
                + timedelta(minutes=10)
            ),
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    response = client.get(
        "/api/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 401