from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text
)
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    history = relationship(
        "History",
        back_populates="user"
    )

    quiz_results = relationship(
        "QuizResult",
        back_populates="user"
    )
    email = Column(
        String,
        unique=True,
        nullable=True
    )



class Category(Base):
    __tablename__ = "categories"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True,
        index=True
    )

    questions = relationship(
        "Question",
        back_populates="category"
    )

    def __str__(self):
        return self.name


class Question(Base):
    __tablename__ = "questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    question_text = Column(
        Text
    )

    correct_answer = Column(
        String
    )

    incorrect_answers = Column(
        JSON
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id")
    )

    difficulty = Column(
        String
    )

    tags = Column(
        JSON,
        default=lambda: ["general"]
    )

    type = Column(
        String,
        default="multiple_choice",
        nullable=False
    )

    media_type = Column(
        String,
        default="text",
        nullable=False
    )

    media_url = Column(
        String,
        nullable=True
    )

    regions = Column(
        JSON,
        default=lambda: ["global"]
    )

    is_niche = Column(
        Boolean,
        default=False
    )

    category = relationship(
        "Category",
        back_populates="questions"
    )

    history_items = relationship(
        "History",
        back_populates="question"
    )

    def __str__(self):
        return self.question_text


class History(Base):
    __tablename__ = "history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False,
        index=True
    )

    is_correct = Column(
        Integer,
        nullable=False
    )

    answered_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="history"
    )

    question = relationship(
        "Question",
        back_populates="history_items"
    )


class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    category = Column(
        String,
        nullable=False
    )

    question_types = Column(
        JSON,
        nullable=False
    )

    question_count = Column(
        Integer,
        nullable=False
    )

    correct_count = Column(
        Integer,
        nullable=False
    )

    score = Column(
        Integer,
        nullable=False
    )

    completed_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="quiz_results"
    )