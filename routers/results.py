from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import QuizResultCreate, QuizResultOut
from crud import create_quiz_result, get_quiz_results
from auth_utils import get_current_user


router = APIRouter(
    prefix="/api/results",
    tags=["results"]
)


@router.post(
    "/",
    response_model=QuizResultOut
)
def create_result(
    payload: QuizResultCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_quiz_result(
        db=db,
        user_id=current_user.id,
        category=payload.category,
        question_types=payload.question_types,
        question_count=payload.question_count,
        correct_count=payload.correct_count
    )


@router.get(
    "/",
    response_model=list[QuizResultOut]
)
def list_results(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_quiz_results(
        db,
        current_user.id
    )