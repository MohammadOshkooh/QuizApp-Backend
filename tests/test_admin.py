import base64

from config import settings

from .conftest import client


def test_admin_requires_authentication():
    response = client.get("/admin")

    assert response.status_code == 401

    assert (
        response.headers["WWW-Authenticate"]
        == 'Basic realm="Quizella Admin"'
    )

    assert (
        response.json()["detail"]
        == "Admin authentication required."
    )


def test_admin_rejects_invalid_credentials():
    credentials = base64.b64encode(
        b"wrong:wrong"
    ).decode()

    response = client.get(
        "/admin",
        headers={
            "Authorization": (
                f"Basic {credentials}"
            )
        },
    )

    assert response.status_code == 401

    assert (
        response.json()["detail"]
        == "Invalid admin credentials."
    )


def test_admin_rejects_malformed_basic_auth():
    response = client.get(
        "/admin",
        headers={
            "Authorization": "Basic !!!invalid!!!"
        },
    )

    assert response.status_code == 401

    assert (
        response.json()["detail"]
        == "Invalid admin credentials."
    )


def test_admin_accepts_valid_credentials():
    credentials = base64.b64encode(
        (
            f"{settings.ADMIN_USERNAME}:"
            f"{settings.ADMIN_PASSWORD}"
        ).encode()
    ).decode()

    response = client.get(
        "/admin",
        headers={
            "Authorization": (
                f"Basic {credentials}"
            )
        },
    )

    assert response.status_code in {
        200,
        302,
        303,
    }