import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = (
    "test-secret-key-that-is-at-least-32-characters-long"
)
os.environ["ADMIN_USERNAME"] = "testadmin"
os.environ["ADMIN_PASSWORD"] = "test-admin-password"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["ALLOWED_HOSTS"] = (
    "testserver,localhost,127.0.0.1"
)
os.environ["CORS_ORIGINS"] = "http://localhost:3000"

from database import Base, get_db
from main import app
from models import Category, Question


TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=TEST_ENGINE,
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=TEST_ENGINE)
    Base.metadata.create_all(bind=TEST_ENGINE)

    from security import (
        answer_rate_limiter,
        login_rate_limiter,
        question_rate_limiter,
        register_rate_limiter,
        result_rate_limiter,
    )

    limiters = [
        answer_rate_limiter,
        login_rate_limiter,
        question_rate_limiter,
        register_rate_limiter,
        result_rate_limiter,
    ]

    for limiter in limiters:
        with limiter._lock:
            limiter._requests.clear()

    yield

    Base.metadata.drop_all(bind=TEST_ENGINE)


@pytest.fixture
def db():
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def registered_user():
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "password": "strongpassword123",
        },
    )

    assert response.status_code == 201

    return response.json()


@pytest.fixture
def auth_token(registered_user):
    response = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "strongpassword123",
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {
        "Authorization": f"Bearer {auth_token}"
    }


@pytest.fixture
def sample_category_and_questions(db):
    category = Category(
        name="Science"
    )

    db.add(category)
    db.flush()

    question1 = Question(
        question_text="What is 2 + 2?",
        correct_answer="4",
        incorrect_answers=[
            "3",
            "5",
            "6",
        ],
        category_id=category.id,
        difficulty="easy",
        tags=["math"],
        type="multiple_choice",
        media_type="text",
        media_url=None,
        regions=["global"],
        is_niche=False,
    )

    question2 = Question(
        question_text="What is the capital of France?",
        correct_answer="Paris",
        incorrect_answers=[
            "London",
            "Berlin",
            "Madrid",
        ],
        category_id=category.id,
        difficulty="easy",
        tags=["geography"],
        type="multiple_choice",
        media_type="text",
        media_url=None,
        regions=["global"],
        is_niche=False,
    )

    db.add_all(
        [
            question1,
            question2,
        ]
    )

    db.commit()

    db.refresh(question1)
    db.refresh(question2)

    return category, question1, question2