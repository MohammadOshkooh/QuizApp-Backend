from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings


connect_args = {}

if settings.DATABASE_URL.startswith(
    "sqlite"
):
    connect_args = {
        "check_same_thread": False,
        "timeout": 30
    }


engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)


if settings.DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


def migrate_schema():
    """
    Apply SQLite schema/data migrations required
    by the current Question model.
    """

    # The current migration code is SQLite-specific.
    if not settings.DATABASE_URL.startswith(
        "sqlite"
    ):
        return

    with engine.begin() as connection:

        columns = connection.execute(
            text(
                "PRAGMA table_info(questions)"
            )
        ).fetchall()

        column_names = {
            row[1]
            for row in columns
        }

        if (
            columns
            and "media_type"
            not in column_names
        ):
            connection.execute(
                text(
                    "ALTER TABLE questions "
                    "ADD COLUMN media_type "
                    "VARCHAR DEFAULT 'text' NOT NULL"
                )
            )

        if (
            columns
            and "media_url"
            not in column_names
        ):
            connection.execute(
                text(
                    "ALTER TABLE questions "
                    "ADD COLUMN media_url VARCHAR"
                )
            )

        if not columns:
            return

        connection.execute(
            text(
                """
                UPDATE questions
                SET media_type = type
                WHERE type IN ('audio', 'image')
                  AND (
                      media_type IS NULL
                      OR media_type = 'text'
                      OR media_type = ''
                  )
                """
            )
        )

        connection.execute(
            text(
                """
                UPDATE questions
                SET type = 'multiple_choice'
                WHERE type IS NULL
                   OR type = ''
                   OR type IN ('audio', 'image')
                """
            )
        )

        connection.execute(
            text(
                "UPDATE questions "
                "SET media_url = "
                "'/media/audio/apple.wav' "
                "WHERE media_url = "
                "'/media/audio/apple.ogg'"
            )
        )

        connection.execute(
            text(
                "UPDATE questions "
                "SET media_url = "
                "'/media/images/cat.png' "
                "WHERE media_url = "
                "'/media/images/cat.jpg'"
            )
        )

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


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()