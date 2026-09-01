from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class QuestionBase(BaseModel):
    question: str
    correctAnswer: str
    incorrectAnswers: List[str]
    category: str
    difficulty: str

    tags: List[str] = ["general"]

    # Every question is multiple choice.
    type: str = "multiple_choice"

    # Content/media type:
    # text / audio / image
    media_type: str = "text"

    # NULL for normal text questions.
    media_url: Optional[str] = None

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


class QuestionOut(BaseModel):
    id: str
    question: str
    correctAnswer: str
    incorrectAnswers: List[str]
    category: str
    difficulty: str

    tags: List[str] = []

    # This remains the answer mechanism.
    type: str = "multiple_choice"

    # This is the actual Question media type.
    mediaType: str = "text"

    # Relative/absolute URL for audio/image.
    mediaUrl: Optional[str] = None

    regions: List[str] = []

    isNiche: bool = False

    class Config:
        from_attributes = True


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