import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine, Base, migrate_schema
from routers import auth, questions, users, categories
from admin import setup_admin

migrate_schema()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="QuizeApp API", version="1.1.0")

setup_admin(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEDIA_DIR = Path(__file__).parent / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")

app.include_router(auth.router)
app.include_router(questions.router)
app.include_router(users.router)
app.include_router(categories.router)


@app.get("/")
def root():
    return {"message": "QuizeApp API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
