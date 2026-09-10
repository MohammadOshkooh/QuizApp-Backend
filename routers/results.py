from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from auth_utils import get_current_user
from config import settings
from crud import create_quiz_result, get_quiz_results
from database import get_db
from schemas import QuizResultCreate, QuizResultOut
from security import result_rate_limiter


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
    result_rate_limiter.check(
        f"result:user:{current_user.id}"
    )

    try:
        token_payload = jwt.decode(
            payload.quiz_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        if token_payload.get("type") != "quiz":
            raise ValueError

        if token_payload.get("sub") != str(current_user.id):
            raise ValueError

        raw_question_ids = token_payload.get(
            "question_ids"
        )

        if not isinstance(raw_question_ids, list):
            raise ValueError

        if not isinstance(
            token_payload.get("iat"),
            (int, float)
        ):
            raise ValueError

        quiz_issued_at = datetime.fromtimestamp(
            float(token_payload["iat"]),
            tz=timezone.utc
        ).replace(tzinfo=None)

        quiz_token_question_ids = {
            int(question_id)
            for question_id in raw_question_ids
        }

        if not quiz_token_question_ids:
            raise ValueError

        return create_quiz_result(
            db=db,
            user_id=current_user.id,
            history_ids=payload.history_ids,
            quiz_token_question_ids=quiz_token_question_ids,
            quiz_issued_at=quiz_issued_at
        )

    except (
        JWTError,
        TypeError,
        ValueError,
        OverflowError
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
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