from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def migrate_schema():
    """
    Apply SQLite schema/data migrations required by the current Question model.
    """
    with engine.begin() as connection:
        columns = connection.execute(
            text("PRAGMA table_info(questions)")
        ).fetchall()

        column_names = {row[1] for row in columns}

        if columns and "media_type" not in column_names:
            connection.execute(
                text(
                    "ALTER TABLE questions "
                    "ADD COLUMN media_type VARCHAR DEFAULT 'text' NOT NULL"
                )
            )

        if columns and "media_url" not in column_names:
            connection.execute(
                text(
                    "ALTER TABLE questions ADD COLUMN media_url VARCHAR"
                )
            )

        if not columns:
            return

        # Older versions stored "audio" or "image" in the
        # Question.type column. The current contract keeps
        # Question.type as "multiple_choice" and stores the
        # media kind separately in media_type.
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

        # Every question in Quizella is multiple choice.
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

        # The actual files contained in the uploaded project are
        # apple.wav and cat.png. The current database snapshot
        # contains old references to apple.ogg and cat.jpg.
        connection.execute(
            text(
                "UPDATE questions "
                "SET media_url = '/media/audio/apple.wav' "
                "WHERE media_url = '/media/audio/apple.ogg'"
            )
        )

        connection.execute(
            text(
                "UPDATE questions "
                "SET media_url = '/media/images/cat.png' "
                "WHERE media_url = '/media/images/cat.jpg'"
            )
        )

        # Any remaining NULL/empty media type belongs to a normal
        # text question.
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