"""Add playable audio/image multiple-choice questions to QuizApp."""

import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from database import SessionLocal, migrate_schema
from models import Category, Question


CATEGORIES = [
    "English",
    "Science",
    "History",
    "Geography",
    "Sports",
    "Literature"
]


def question_data(
    category: str,
    question_type: str
):
    if question_type == "audio":
        return {
            "question": (
                f"[{category}] Which word did you hear?"
            ),
            "correctAnswer": "Apple",
            "incorrectAnswers": [
                "Orange",
                "Banana",
                "Grape"
            ],
            "category": category,
            "difficulty": "easy",
            "tags": [
                "listening",
                "vocabulary"
            ],

            # All questions remain multiple choice.
            "type": "multiple_choice",

            # This is the media/content type.
            "mediaType": "audio",

            "mediaUrl": (
                "/media/audio/apple.wav"
            ),

            "regions": [
                "global"
            ],

            "isNiche": False
        }

    return {
        "question": (
            f"[{category}] Which animal is shown?"
        ),
        "correctAnswer": "Cat",
        "incorrectAnswers": [
            "Dog",
            "Lion",
            "Tiger"
        ],
        "category": category,
        "difficulty": "easy",
        "tags": [
            "animals",
            "visual"
        ],

        "type": "multiple_choice",

        "mediaType": "image",

        "mediaUrl": (
            "/media/images/cat.png"
        ),

        "regions": [
            "global"
        ],

        "isNiche": False
    }


def seed_media_questions():
    migrate_schema()

    db = SessionLocal()

    try:
        added = 0
        updated = 0

        for category_name in CATEGORIES:

            category = (
                db.query(Category)
                .filter(
                    Category.name == category_name
                )
                .first()
            )

            if not category:
                category = Category(
                    name=category_name
                )

                db.add(category)
                db.flush()

            for question_type in (
                "audio",
                "image"
            ):
                data = question_data(
                    category_name,
                    question_type
                )

                existing = (
                    db.query(Question)
                    .filter(
                        Question.question_text
                        == data["question"],

                        Question.category_id
                        == category.id,

                        Question.media_type
                        == data["mediaType"]
                    )
                    .first()
                )

                if existing:
                    changed = False

                    if existing.type != "multiple_choice":
                        existing.type = "multiple_choice"
                        changed = True

                    if (
                        existing.media_type
                        != data["mediaType"]
                    ):
                        existing.media_type = (
                            data["mediaType"]
                        )
                        changed = True

                    if (
                        existing.media_url
                        != data["mediaUrl"]
                    ):
                        existing.media_url = (
                            data["mediaUrl"]
                        )
                        changed = True

                    if changed:
                        updated += 1

                    continue

                db.add(
                    Question(
                        question_text=data["question"],
                        correct_answer=data["correctAnswer"],
                        incorrect_answers=data[
                            "incorrectAnswers"
                        ],
                        category_id=category.id,
                        difficulty=data["difficulty"],
                        tags=data["tags"],

                        # Always multiple choice.
                        type="multiple_choice",

                        # Actual media type.
                        media_type=data["mediaType"],

                        media_url=data["mediaUrl"],

                        regions=data["regions"],
                        is_niche=data["isNiche"]
                    )
                )

                added += 1

        db.commit()

        print(
            f"Added {added} media questions; "
            f"updated {updated} existing questions."
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_media_questions()