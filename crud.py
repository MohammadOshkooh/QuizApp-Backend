from sqlalchemy.orm import Session
from models import User, Category, Question, History
from schemas import UserCreate, QuestionBase
from auth import hash_password
import random


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    hashed = hash_password(user.password)
    db_user = User(username=user.username, hashed_password=hashed, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_category(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()


def create_category(db: Session, name: str):
    cat = Category(name=name)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


def create_question(db: Session, q: QuestionBase):
    cat = get_category(db, q.category)
    if not cat:
        cat = create_category(db, q.category)

    db_q = Question(
        question_text=q.question,
        correct_answer=q.correctAnswer,
        incorrect_answers=q.incorrectAnswers,
        category_id=cat.id,
        difficulty=q.difficulty,
        tags=q.tags,
        type=q.type,
        regions=q.regions,
        is_niche=q.isNiche
    )
    db.add(db_q)
    db.commit()
    db.refresh(db_q)
    return db_q


def get_questions(db: Session, limit: int = 10, category: str = None, difficulty: str = None):
    query = db.query(Question)
    if category:
        cat = get_category(db, category)
        if cat:
            query = query.filter(Question.category_id == cat.id)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)

    questions = query.limit(limit).all()
    return questions


def get_question(db: Session, qid: int):
    return db.query(Question).filter(Question.id == qid).first()


def save_history(db: Session, user_id: int, question_id: int, is_correct: bool):
    h = History(user_id=user_id, question_id=question_id, is_correct=1 if is_correct else 0)
    db.add(h)
    db.commit()
    return h