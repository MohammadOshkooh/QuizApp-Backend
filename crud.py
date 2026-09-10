from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth import hash_password
from models import (
    Category,
    History,
    Question,
    QuizResult,
    User
)
from schemas import (
    QuestionBase,
    UserCreate
)


def get_user(
    db: Session,
    username: str
):
    return (
        db.query(User)
        .filter(
            User.username == username
        )
        .first()
    )


def get_user_by_id(
    db: Session,
    user_id: int
):
    return (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )


def create_user(
    db: Session,
    user: UserCreate
):
    hashed = hash_password(
        user.password
    )

    db_user = User(
        username=user.username,
        hashed_password=hashed
    )

    db.add(db_user)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise

    db.refresh(db_user)

    return db_user


def get_category(
    db: Session,
    name: str
):
    return (
        db.query(Category)
        .filter(
            Category.name == name
        )
        .first()
    )


def get_categories(
    db: Session
):
    return (
        db.query(Category)
        .order_by(Category.id)
        .all()
    )


def create_category(
    db: Session,
    name: str
):
    category = Category(
        name=name
    )

    db.add(category)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise

    db.refresh(category)

    return category


def create_question(
    db: Session,
    q: QuestionBase
):
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

    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise

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
                Question.category_id
                == category_obj.id
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
        .filter(
            Question.id == qid
        )
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

    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise

    db.refresh(history)

    return history


def create_quiz_result(
    db: Session,
    user_id: int,
    history_ids: list[int],
    quiz_token_question_ids: set[int],
    quiz_issued_at
):
    histories = (
        db.query(History)
        .filter(
            History.user_id == user_id,
            History.id.in_(history_ids)
        )
        .all()
    )

    if len(histories) != len(history_ids):
        raise ValueError(
            "One or more answer records do not belong to the current user."
        )

    if any(
        history.answered_at < quiz_issued_at
        for history in histories
    ):
        raise ValueError(
            "Quiz results can only contain answers from the current quiz session."
        )

    history_by_id = {
        history.id: history
        for history in histories
    }

    ordered_histories = [
        history_by_id[history_id]
        for history_id in history_ids
    ]

    question_ids = {
        history.question_id
        for history in ordered_histories
    }

    if not question_ids.issubset(quiz_token_question_ids):
        raise ValueError(
            "Answer records do not belong to the quiz session."
        )

    if len(question_ids) != len(ordered_histories):
        raise ValueError(
            "Each question can only appear once in a quiz result."
        )

    if question_ids != quiz_token_question_ids:
        raise ValueError(
            "Quiz result is incomplete or does not match the quiz session."
        )

    questions = (
        db.query(Question)
        .filter(
            Question.id.in_(list(question_ids))
        )
        .all()
    )

    if len(questions) != len(question_ids):
        raise ValueError(
            "One or more questions no longer exist."
        )

    question_by_id = {
        question.id: question
        for question in questions
    }

    categories = {
        question_by_id[history.question_id].category.name
        for history in ordered_histories
        if question_by_id[history.question_id].category
    }

    if len(categories) != 1:
        raise ValueError(
            "All questions in a quiz result must belong to one category."
        )

    question_types = sorted({
        question_by_id[history.question_id].media_type
        for history in ordered_histories
    })

    question_count = len(ordered_histories)

    correct_count = sum(
        1
        for history in ordered_histories
        if bool(history.is_correct)
    )

    result = QuizResult(
        user_id=user_id,
        category=next(iter(categories)),
        question_types=question_types,
        question_count=question_count,
        correct_count=correct_count,
        score=correct_count
    )

    db.add(result)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise

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