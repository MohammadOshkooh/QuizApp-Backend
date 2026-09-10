from datetime import datetime
from typing import List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator
)


class QuestionBase(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000
    )

    correctAnswer: str = Field(
        min_length=1,
        max_length=500
    )

    incorrectAnswers: List[str] = Field(
        min_length=1,
        max_length=10
    )

    category: str = Field(
        min_length=1,
        max_length=100
    )

    difficulty: str = Field(
        min_length=1,
        max_length=30
    )

    tags: List[str] = Field(
        default_factory=lambda: ["general"],
        max_length=20
    )

    type: str = Field(
        default="multiple_choice",
        max_length=50
    )

    media_type: str = Field(
        default="text",
        alias="mediaType",
        max_length=20
    )

    media_url: Optional[str] = Field(
        default=None,
        alias="mediaUrl",
        max_length=500
    )

    regions: List[str] = Field(
        default_factory=lambda: ["global"],
        max_length=20
    )

    isNiche: bool = False

    model_config = ConfigDict(
        populate_by_name=True
    )

    @field_validator(
        "question",
        "correctAnswer",
        "category",
        "difficulty",
        "type",
        "media_type"
    )
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Value cannot be empty."
            )

        return value

    @field_validator("incorrectAnswers")
    @classmethod
    def clean_incorrect_answers(
        cls,
        values: List[str]
    ) -> List[str]:
        cleaned = [value.strip() for value in values]

        if any(not value for value in cleaned):
            raise ValueError(
                "Answers cannot be empty."
            )

        if len(set(cleaned)) != len(cleaned):
            raise ValueError(
                "Answers must be unique."
            )

        return cleaned


class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=30,
        pattern=r"^[A-Za-z0-9_.-]+$"
    )

    password: str = Field(
        min_length=8,
        max_length=72
    )

    @field_validator("username")
    @classmethod
    def normalize_username(
        cls,
        value: str
    ) -> str:
        return value.strip()

    @field_validator("password")
    @classmethod
    def validate_password_bytes(
        cls,
        value: str
    ) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError(
                "Password cannot be longer than 72 UTF-8 bytes."
            )

        return value


class UserLogin(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=30
    )

    password: str = Field(
        min_length=1,
        max_length=72
    )

    @field_validator("username")
    @classmethod
    def normalize_username(
        cls,
        value: str
    ) -> str:
        return value.strip()

    @field_validator("password")
    @classmethod
    def validate_password_bytes(
        cls,
        value: str
    ) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError(
                "Password cannot be longer than 72 UTF-8 bytes."
            )

        return value


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class CategoryOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )


class QuestionOut(BaseModel):
    id: str
    question: str
    answers: List[str]
    quizToken: str

    category: str
    difficulty: str

    tags: List[str] = Field(
        default_factory=list
    )

    type: str = "multiple_choice"

    media_type: str = Field(
        default="text",
        alias="mediaType"
    )

    media_url: Optional[str] = Field(
        default=None,
        alias="mediaUrl"
    )

    regions: List[str] = Field(
        default_factory=list
    )

    isNiche: bool = False

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class AnswerSubmit(BaseModel):
    question_id: int = Field(
        ge=1
    )

    quiz_token: str = Field(
        min_length=1,
        max_length=4000
    )

    selected_answer: str = Field(
        min_length=1,
        max_length=500
    )

    @field_validator("selected_answer")
    @classmethod
    def clean_answer(
        cls,
        value: str
    ) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Selected answer cannot be empty."
            )

        return value


class AnswerResult(BaseModel):
    correct: bool
    correct_answer: str
    history_id: int


class HistoryOut(BaseModel):
    id: int
    question_id: int
    is_correct: bool
    answered_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class StatsOut(BaseModel):
    total_games: int
    total_questions: int
    correct_count: int
    accuracy: float


class QuizResultCreate(BaseModel):
    # The client no longer sends a score. The backend calculates the score
    # from authenticated user's answer-history records.
    quiz_token: str = Field(
        min_length=1,
        max_length=4000
    )

    history_ids: List[int] = Field(
        min_length=1,
        max_length=100
    )

    @field_validator("history_ids")
    @classmethod
    def validate_history_ids(
        cls,
        values: List[int]
    ) -> List[int]:
        if len(set(values)) != len(values):
            raise ValueError(
                "History IDs must be unique."
            )

        return values


class QuizResultOut(BaseModel):
    id: int
    category: str
    question_types: List[str]
    question_count: int
    correct_count: int
    score: int
    completed_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )