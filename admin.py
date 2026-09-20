from fastapi import FastAPI
from sqladmin import Admin, ModelView

from database import engine
from models import (
    Category,
    History,
    Question,
    User,
    QuizResult
)


class UserAdmin(ModelView, model=User):

    column_list = [
        User.id,
        User.username,
        User.email,
        User.created_at
    ]

    column_searchable_list = [
        User.username,
        User.email
    ]

    form_excluded_columns = [
        User.hashed_password
    ]


class QuestionAdmin(ModelView, model=Question):

    column_list = [
        Question.id,
        Question.question_text,
        Question.difficulty,
        Question.category,
        Question.tags,
        Question.type,
        Question.media_type,
        Question.media_url,
        Question.regions,
        Question.is_niche
    ]

    column_searchable_list = [
        Question.question_text
    ]


class CategoryAdmin(ModelView, model=Category):

    column_list = [
        Category.id,
        Category.name
    ]

    column_searchable_list = [
        Category.name
    ]


class HistoryAdmin(ModelView, model=History):

    column_list = [
        History.id,
        History.user_id,
        History.question_id,
        History.is_correct,
        History.answered_at
    ]

    # Audit data - should not be modified manually
    can_create = False
    can_edit = False
    can_delete = False


class QuizResultAdmin(ModelView, model=QuizResult):

    column_list = [
        QuizResult.id,
        QuizResult.user_id,
        QuizResult.category,
        QuizResult.question_types,
        QuizResult.question_count,
        QuizResult.correct_count,
        QuizResult.score,
        QuizResult.completed_at
    ]

    column_searchable_list = [
        QuizResult.category
    ]

    # Results are generated from user answers
    # Prevent manual score manipulation
    can_create = False
    can_edit = False
    can_delete = False



def setup_admin(app: FastAPI):

    admin = Admin(
        app,
        engine,
        title="QuizApp Admin Panel"
    )

    admin.add_view(UserAdmin)

    admin.add_view(CategoryAdmin)

    admin.add_view(QuestionAdmin)

    admin.add_view(HistoryAdmin)

    admin.add_view(QuizResultAdmin)

    return admin