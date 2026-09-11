import pytest

from models import Question

from .conftest import client, TestingSessionLocal


def test_questions_requires_authentication():
    response = client.get(
        "/api/questions/"
    )

    assert response.status_code == 401


def test_list_questions(
    auth_headers,
    sample_category_and_questions,
):
    response = client.get(
        "/api/questions/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    for question in data:
        assert "id" in question
        assert "question" in question
        assert "answers" in question
        assert "quizToken" in question
        assert "category" in question
        assert "difficulty" in question

        assert "correctAnswer" not in question
        assert "correct_answer" not in question

        assert len(question["answers"]) == 4
        assert question["type"] == "multiple_choice"
        assert question["mediaType"] == "text"


def test_question_limit(
    auth_headers,
    sample_category_and_questions,
):
    response = client.get(
        "/api/questions/?limit=1",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.parametrize(
    "limit",
    [
        0,
        51,
    ],
)
def test_question_limit_validation(
    auth_headers,
    limit,
):
    response = client.get(
        f"/api/questions/?limit={limit}",
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_filter_by_category(
    auth_headers,
    sample_category_and_questions,
):
    response = client.get(
        "/api/questions/?category=Science",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    for question in data:
        assert question["category"] == "Science"


def test_unknown_category_returns_empty(
    auth_headers,
    sample_category_and_questions,
):
    response = client.get(
        "/api/questions/?category=Unknown",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == []


def test_filter_by_difficulty(
    auth_headers,
    sample_category_and_questions,
):
    response = client.get(
        "/api/questions/?difficulty=easy",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_correct_answer_is_not_exposed(
    auth_headers,
    sample_category_and_questions,
):
    response = client.get(
        "/api/questions/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    for item in response.json():
        assert "correctAnswer" not in item
        assert "correct_answer" not in item


def test_question_answers_contain_valid_choices(
    auth_headers,
    sample_category_and_questions,
):
    response = client.get(
        "/api/questions/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    for item in response.json():
        db = None
        try:

            db = TestingSessionLocal()

            question = (
                db.query(Question)
                .filter(
                    Question.id == int(item["id"])
                )
                .first()
            )

            assert question is not None

            expected = {
                question.correct_answer,
                *(
                    question.incorrect_answers
                    or []
                ),
            }

            assert set(item["answers"]) == expected

        finally:
            if db is not None:
                db.close()


def test_answer_question_correct(
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

    data = response.json()

    assert data["correct"] is True
    assert data["correct_answer"] == correct_answer
    assert data["history_id"] > 0


def test_answer_question_wrong(
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

        wrong_answer = (
            db_question.incorrect_answers[0]
        )

    finally:
        db.close()

    response = client.post(
        "/api/questions/answer",
        headers=auth_headers,
        json={
            "question_id": int(question["id"]),
            "quiz_token": question["quizToken"],
            "selected_answer": wrong_answer,
        },
    )

    assert response.status_code == 200
    assert response.json()["correct"] is False


def test_invalid_selected_answer(
    auth_headers,
    sample_category_and_questions,
):
    questions = client.get(
        "/api/questions/",
        headers=auth_headers,
    ).json()

    question = questions[0]

    response = client.post(
        "/api/questions/answer",
        headers=auth_headers,
        json={
            "question_id": int(question["id"]),
            "quiz_token": question["quizToken"],
            "selected_answer": "INVALID ANSWER",
        },
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Selected answer is not valid for this question."
    )


def test_same_question_cannot_be_answered_twice(
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

    payload = {
        "question_id": int(question["id"]),
        "quiz_token": question["quizToken"],
        "selected_answer": correct_answer,
    }

    first = client.post(
        "/api/questions/answer",
        headers=auth_headers,
        json=payload,
    )

    assert first.status_code == 200

    second = client.post(
        "/api/questions/answer",
        headers=auth_headers,
        json=payload,
    )

    assert second.status_code == 409


def test_invalid_quiz_token(
    auth_headers,
    sample_category_and_questions,
):
    response = client.post(
        "/api/questions/answer",
        headers=auth_headers,
        json={
            "question_id": 1,
            "quiz_token": "invalid-token",
            "selected_answer": "4",
        },
    )

    assert response.status_code == 400