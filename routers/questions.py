from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from database import get_db
from schemas import (
    QuestionOut,
    AnswerSubmit,
    AnswerResult
)
from crud import (
    get_questions,
    get_question,
    save_history
)
from auth_utils import get_current_user


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
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    media_types: Optional[List[str]] = Query(
        None
    ),
    db: Session = Depends(get_db)
):
    questions = get_questions(
        db=db,
        limit=limit,
        category=category,
        difficulty=difficulty,
        media_types=media_types
    )

    return [
        {
            "id": str(question.id),
            "question": question.question_text,
            "correctAnswer": question.correct_answer,
            "incorrectAnswers": (
                question.incorrect_answers
                if question.incorrect_answers
                else []
            ),
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


@router.post(
    "/answer",
    response_model=AnswerResult
)
def answer_question(
    payload: AnswerSubmit,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    question = get_question(
        db,
        payload.question_id
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    correct = (
        payload.selected_answer
        == question.correct_answer
    )

    save_history(
        db,
        user.id,
        question.id,
        correct
    )

    return {
        "correct": correct,
        "correct_answer": question.correct_answer
    }