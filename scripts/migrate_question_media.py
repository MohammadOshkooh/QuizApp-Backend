import sys
import os

# Add backend root to Python path.
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from sqlalchemy import inspect, text
from database import engine


def migrate():
    inspector = inspect(engine)

    table_names = inspector.get_table_names()

    if "questions" not in table_names:
        print(
            "questions table does not exist. "
            "It will be created by the application."
        )
        return

    existing_columns = {
        column["name"]
        for column in inspector.get_columns(
            "questions"
        )
    }

    with engine.begin() as connection:

        if "media_type" not in existing_columns:
            print(
                "Adding media_type column..."
            )

            connection.execute(
                text(
                    """
                    ALTER TABLE questions
                    ADD COLUMN media_type VARCHAR
                    DEFAULT 'text'
                    """
                )
            )

        else:
            print(
                "media_type already exists."
            )

        if "media_url" not in existing_columns:
            print(
                "Adding media_url column..."
            )

            connection.execute(
                text(
                    """
                    ALTER TABLE questions
                    ADD COLUMN media_url VARCHAR
                    """
                )
            )

        else:
            print(
                "media_url already exists."
            )

        # Existing questions are all multiple choice.
        connection.execute(
            text(
                """
                UPDATE questions
                SET type = 'multiple_choice'
                WHERE type IS NULL
                   OR type = ''
                """
            )
        )

        # Existing questions are text questions.
        connection.execute(
            text(
                """
                UPDATE questions
                SET media_type = 'text'
                WHERE media_type IS NULL
                   OR media_type = ''
                """
            )
        )

    print(
        "Question media migration completed successfully."
    )


if __name__ == "__main__":
    migrate()