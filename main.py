import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, questions, users

from admin import setup_admin

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI(title="QuizeApp API", version="1.0.0")

admin = setup_admin(app)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(questions.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "QuizeApp API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}