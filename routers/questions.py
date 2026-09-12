from datetime import datetime, timedelta, timezone
from random import SystemRandom
from secrets import token_urlsafe
from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)
from sqlalchemy.orm import Session

from jose import JWTError, jwt

from auth_utils import get_current_user
from config import settings
from crud import (
    get_question,
    get_questions,
    save_history
)
from database import get_db
from models import History
from schemas import (
    AnswerResult,
    AnswerSubmit,
    QuestionOut
)
from security import (
    answer_rate_limiter,
    question_rate_limiter
)


randomizer = SystemRandom()


router = APIRouter(
    prefix="/api/questions",
    tags=["questions"]
)


@router.get(
    "/",
    response_model=List[QuestionOut]
)
def list_questions(
    limit: int = Query(
        10,
        ge=1,
        le=50
    ),
    category: Optional[str] = Query(
        None,
        max_length=100
    ),
    difficulty: Optional[str] = Query(
        None,
        max_length=30
    ),
    media_types: Optional[List[str]] = Query(
        None,
        max_length=3
    ),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):


    question_rate_limiter.check(
        f"questions:user:{user.id}"
    )

    questions = get_questions(
        db=db,
        limit=limit,
        category=category.strip() if category else None,
        difficulty=difficulty.strip() if difficulty else None,
        media_types=media_types
    )

    question_ids = [
        question.id
        for question in questions
    ]

    quiz_token = jwt.encode(
        {
            "sub": str(user.id),
            "type": "quiz",
            "jti": token_urlsafe(16),
            "question_ids": question_ids,
            "iat": datetime.now(timezone.utc),
            "exp": (
                datetime.now(timezone.utc)
                + timedelta(minutes=60)
            )
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    def shuffle_answers(question):
        answers = [
            question.correct_answer,
            *(question.incorrect_answers or [])
        ]

        randomizer.shuffle(answers)

        return answers

    return [
        {
            "id": str(question.id),
            "question": (
                question.question_text
            ),
            "quizToken": quiz_token,

            "answers": shuffle_answers(question),

            "category": (
                question.category.name
                if question.category
                else "Unknown"
            ),

            "difficulty": question.difficulty,

            "tags": (
                question.tags
                if question.tags
                else []
            ),

            "type": (
                question.type
                if question.type
                else "multiple_choice"
            ),

            "mediaType": (
                question.media_type
                if question.media_type
                else "text"
            ),

            "mediaUrl": question.media_url,

            "regions": (
                question.regions
                if question.regions
                else []
            ),

            "isNiche": (
                question.is_niche
                if question.is_niche is not None
                else False
            )
        }
        for question in questions
    ]


def verify_quiz_token(
    token: str,
    user_id: int,
    question_id: int
) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        if payload.get("type") != "quiz":
            raise ValueError

        if payload.get("sub") != str(user_id):
            raise ValueError

        question_ids = payload.get("question_ids")

        if not isinstance(question_ids, list):
            raise ValueError

        if question_id not in {
            int(question_id)
            for question_id in question_ids
        }:
            raise ValueError

        if not isinstance(
            payload.get("iat"),
            (int, float)
        ):
            raise ValueError

        return payload

    except (
        JWTError,
        TypeError,
        ValueError,
        OverflowError
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired quiz session."
        )


@router.post(
    "/answer",
    response_model=AnswerResult
)
def answer_question(
    payload: AnswerSubmit,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    answer_rate_limiter.check(
        f"answer:user:{user.id}"
    )

    quiz_payload = verify_quiz_token(
        payload.quiz_token,
        user.id,
        payload.question_id
    )

    issued_at = datetime.fromtimestamp(
        float(quiz_payload["iat"]),
        tz=timezone.utc
    ).replace(tzinfo=None)

    existing_answer = (
        db.query(
            History
        )
        .filter(
            History.user_id == user.id,
            History.question_id == payload.question_id,
            History.answered_at >= issued_at
        )
        .first()
    )

    if existing_answer is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This question has already been answered in this quiz."
        )

    question = get_question(
        db,
        payload.question_id
    )

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found."
        )

    allowed_answers = {
        question.correct_answer,
        *(
            question.incorrect_answers
            if question.incorrect_answers
            else []
        )
    }

    if payload.selected_answer not in allowed_answers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Selected answer is not valid for this question."
        )

    correct = (
        payload.selected_answer
        == question.correct_answer
    )

    history = save_history(
        db,
        user.id,
        question.id,
        correct
    )

    return {
        "correct": correct,
        "correct_answer": question.correct_answer,
        "history_id": history.id
    }