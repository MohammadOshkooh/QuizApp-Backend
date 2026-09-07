from sqlalchemy.orm import Session

from models import User, Category, Question, History, QuizResult
from schemas import UserCreate, QuestionBase
from auth import hash_password


def get_user(db: Session, username: str):
    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )


def create_user(db: Session, user: UserCreate):
    hashed = hash_password(user.password)

    db_user = User(
        username=user.username,
        hashed_password=hashed,
        email=user.email
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_category(db: Session, name: str):
    return (
        db.query(Category)
        .filter(Category.name == name)
        .first()
    )


def get_categories(db: Session):
    return (
        db.query(Category)
        .order_by(Category.id)
        .all()
    )


def create_category(db: Session, name: str):
    category = Category(
        name=name
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def create_question(db: Session, q: QuestionBase):
    category = get_category(
        db,
        q.category
    )

    if not category:
        category = create_category(
            db,
            q.category
        )

    db_question = Question(
        question_text=q.question,
        correct_answer=q.correctAnswer,
        incorrect_answers=q.incorrectAnswers,
        category_id=category.id,
        difficulty=q.difficulty,
        tags=q.tags,
        type="multiple_choice",
        media_type=q.media_type,
        media_url=q.media_url,
        regions=q.regions,
        is_niche=q.isNiche
    )

    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    return db_question

def get_questions(
    db: Session,
    limit: int = 10,
    category: str = None,
    difficulty: str = None,
    media_types: list[str] = None
):
    query = db.query(Question)

    query = query.filter(
        Question.type == "multiple_choice"
    )

    if category:
        category_obj = get_category(
            db,
            category
        )

        if category_obj:
            query = query.filter(
                Question.category_id == category_obj.id
            )

    if difficulty:
        query = query.filter(
            Question.difficulty == difficulty
        )

    if media_types:
        valid_media_types = {
            media_type
            for media_type in media_types
            if media_type in {
                "text",
                "audio",
                "image"
            }
        }

        if valid_media_types:
            query = query.filter(
                Question.media_type.in_(
                    list(valid_media_types)
                )
            )

    return (
        query
        .order_by(Question.id)
        .limit(limit)
        .all()
    )


def get_question(
    db: Session,
    qid: int
):
    return (
        db.query(Question)
        .filter(Question.id == qid)
        .first()
    )


def save_history(
    db: Session,
    user_id: int,
    question_id: int,
    is_correct: bool
):
    history = History(
        user_id=user_id,
        question_id=question_id,
        is_correct=1 if is_correct else 0
    )

    db.add(history)
    db.commit()

    return history


def create_quiz_result(
    db: Session,
    user_id: int,
    category: str,
    question_types: list[str],
    question_count: int,
    correct_count: int
):
    result = QuizResult(
        user_id=user_id,
        category=category,
        question_types=question_types,
        question_count=question_count,
        correct_count=correct_count,
        score=correct_count
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return result


def get_quiz_results(
    db: Session,
    user_id: int
):
    return (
        db.query(QuizResult)
        .filter(
            QuizResult.user_id == user_id
        )
        .order_by(
            QuizResult.completed_at.desc(),
            QuizResult.id.desc()
        )
        .all()
    )