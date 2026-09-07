from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class QuestionBase(BaseModel):
    question: str
    correctAnswer: str
    incorrectAnswers: List[str]
    category: str
    difficulty: str

    tags: List[str] = ["general"]

    type: str = "multiple_choice"

    media_type: str = Field(
        default="text",
        alias="mediaType"
    )

    media_url: Optional[str] = Field(
        default=None,
        alias="mediaUrl"
    )

    regions: List[str] = ["global"]

    isNiche: bool = False


class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class QuestionOut(QuestionBase):
    id: str

    tags: List[str] = []

    type: str = "multiple_choice"

    media_type: str = Field(
        default="text",
        alias="mediaType"
    )

    media_url: Optional[str] = Field(
        default=None,
        alias="mediaUrl"
    )

    regions: List[str] = []

    isNiche: bool = False

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class AnswerSubmit(BaseModel):
    question_id: int
    selected_answer: str


class AnswerResult(BaseModel):
    correct: bool
    correct_answer: str


class HistoryOut(BaseModel):
    id: int
    question_id: int
    is_correct: bool
    answered_at: datetime

    class Config:
        from_attributes = True


class StatsOut(BaseModel):
    total_games: int
    total_questions: int
    correct_count: int
    accuracy: float


class QuizResultCreate(BaseModel):
    category: str
    question_types: List[str]
    question_count: int
    correct_count: int


class QuizResultOut(BaseModel):
    id: int
    category: str
    question_types: List[str]
    question_count: int
    correct_count: int
    score: int
    completed_at: datetime

    class Config:
        from_attributes = True