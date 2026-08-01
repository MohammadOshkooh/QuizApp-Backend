from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
from schemas import QuestionOut, AnswerSubmit, AnswerResult
from crud import get_questions, get_question, save_history
from auth_utils import get_current_user

router = APIRouter(prefix="/api/questions", tags=["questions"])

@router.get("/", response_model=List[QuestionOut])
def list_questions(
    limit: int = Query(10, ge=1, le=50),
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return get_questions(db, limit, category, difficulty)

@router.post("/answer", response_model=AnswerResult)
def answer_question(
    payload: AnswerSubmit,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    q = get_question(db, payload.question_id)
    if not q:
        raise HTTPException(404, "Question not found")
    correct = payload.selected_answer == q.correct_answer
    save_history(db, user.id, q.id, correct)
    return {"correct": correct, "correct_answer": q.correct_answer}