from models import Question

from .conftest import client, TestingSessionLocal

def test_results_requires_authentication():
    response = client.get(
        "/api/results/"
    )

    assert response.status_code == 401


def test_empty_results(
    auth_headers,
):
    response = client.get(
        "/api/results/",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == []


def test_create_result_end_to_end(
    auth_headers,
    sample_category_and_questions,
):
    questions = client.get(
        "/api/questions/",
        headers=auth_headers,
    ).json()

    history_ids = []

    for question in questions:
        db = TestingSessionLocal()

        try:
            db_question = (
                db.query(Question)
                .filter(
                    Question.id == int(question["id"])
                )
                .first()
            )

            correct_answer = db_question.correct_answer

        finally:
            db.close()

        response = client.post(
            "/api/questions/answer",
            headers=auth_headers,
            json={
                "question_id": int(question["id"]),
                "quiz_token": question["quizToken"],
                "selected_answer": correct_answer,
            },
        )

        assert response.status_code == 200

        history_ids.append(
            response.json()["history_id"]
        )

    response = client.post(
        "/api/results/",
        headers=auth_headers,
        json={
            "quiz_token": questions[0]["quizToken"],
            "history_ids": history_ids,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["category"] == "Science"
    assert data["question_count"] == 2
    assert data["correct_count"] == 2
    assert data["score"] == 2
    assert "question_types" in data
    assert "completed_at" in data


def test_duplicate_history_ids_are_rejected(
    auth_headers,
    sample_category_and_questions,
):
    questions = client.get(
        "/api/questions/",
        headers=auth_headers,
    ).json()

    question = questions[0]

    db = TestingSessionLocal()

    try:
        db_question = (
            db.query(Question)
            .filter(
                Question.id == int(question["id"])
            )
            .first()
        )

        correct_answer = db_question.correct_answer

    finally:
        db.close()

    answer = client.post(
        "/api/questions/answer",
        headers=auth_headers,
        json={
            "question_id": int(question["id"]),
            "quiz_token": question["quizToken"],
            "selected_answer": correct_answer,
        },
    )

    history_id = answer.json()["history_id"]

    response = client.post(
        "/api/results/",
        headers=auth_headers,
        json={
            "quiz_token": question["quizToken"],
            "history_ids": [
                history_id,
                history_id,
            ],
        },
    )

    assert response.status_code == 422


def test_incomplete_result_is_rejected(
    auth_headers,
    sample_category_and_questions,
):
    questions = client.get(
        "/api/questions/",
        headers=auth_headers,
    ).json()

    question = questions[0]



    db = TestingSessionLocal()

    try:
        db_question = (
            db.query(Question)
            .filter(
                Question.id == int(question["id"])
            )
            .first()
        )

        correct_answer = db_question.correct_answer

    finally:
        db.close()

    answer = client.post(
        "/api/questions/answer",
        headers=auth_headers,
        json={
            "question_id": int(question["id"]),
            "quiz_token": question["quizToken"],
            "selected_answer": correct_answer,
        },
    )

    history_id = answer.json()["history_id"]

    response = client.post(
        "/api/results/",
        headers=auth_headers,
        json={
            "quiz_token": question["quizToken"],
            "history_ids": [history_id],
        },
    )

    assert response.status_code == 400


def test_results_only_belong_to_current_user(
    auth_headers,
    sample_category_and_questions,
):
    questions = client.get(
        "/api/questions/",
        headers=auth_headers,
    ).json()

    question = questions[0]


    db = TestingSessionLocal()

    try:
        db_question = (
            db.query(Question)
            .filter(
                Question.id == int(question["id"])
            )
            .first()
        )

        correct_answer = db_question.correct_answer

    finally:
        db.close()

    answer = client.post(
        "/api/questions/answer",
        headers=auth_headers,
        json={
            "question_id": int(question["id"]),
            "quiz_token": question["quizToken"],
            "selected_answer": correct_answer,
        },
    )

    history_id = answer.json()["history_id"]

    second_register = client.post(
        "/api/auth/register",
        json={
            "username": "seconduser",
            "password": "password123",
        },
    )

    assert second_register.status_code == 201

    second_login = client.post(
        "/api/auth/login",
        json={
            "username": "seconduser",
            "password": "password123",
        },
    )

    second_headers = {
        "Authorization": (
            "Bearer "
            + second_login.json()["access_token"]
        )
    }

    response = client.post(
        "/api/results/",
        headers=second_headers,
        json={
            "quiz_token": question["quizToken"],
            "history_ids": [history_id],
        },
    )

    assert response.status_code == 400