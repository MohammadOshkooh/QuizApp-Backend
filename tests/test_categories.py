from models import Category

from .conftest import client


def test_list_categories_empty():
    response = client.get(
        "/api/categories/"
    )

    assert response.status_code == 200
    assert response.json() == []


def test_list_categories(db):
    db.add_all(
        [
            Category(name="Science"),
            Category(name="History"),
        ]
    )

    db.commit()

    response = client.get(
        "/api/categories/"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Science"
    assert data[1]["name"] == "History"


def test_categories_are_public():
    response = client.get(
        "/api/categories/"
    )

    assert response.status_code != 401