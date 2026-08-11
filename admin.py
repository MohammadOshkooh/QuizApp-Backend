from sqladmin import Admin, ModelView
from fastapi import FastAPI
from database import engine
from models import User, Question, Category, History

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.created_at]
    column_searchable_list = [User.username]

class QuestionAdmin(ModelView, model=Question):
    column_list = [
        Question.id,
        Question.question_text,
        Question.difficulty,
        Question.category,
        Question.tags,
        Question.type,
        Question.regions,
        Question.is_niche
    ]
    column_searchable_list = [Question.question_text]

class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.name]

class HistoryAdmin(ModelView, model=History):
    column_list = [History.id, History.user_id, History.question_id, History.is_correct, History.answered_at]

def setup_admin(app: FastAPI):
    admin = Admin(app, engine, title="Quizella Admin Panel")
    admin.add_view(UserAdmin)
    admin.add_view(QuestionAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(HistoryAdmin)
    return admin