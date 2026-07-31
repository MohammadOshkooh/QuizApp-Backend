from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class QuestionBase(BaseModel):
    question: str
    correctAnswer: str
    incorrectAnswers: List[str]
    category: str
    difficulty: str

class QuestionOut(QuestionBase):
    id: int

class AnswerSubmit(BaseModel):
    question_id: int
    selected_answer: str

class AnswerResult(BaseModel):
    correct: bool
    correct_answer: str