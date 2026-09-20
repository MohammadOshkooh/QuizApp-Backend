# Quizapp Backend 🎯

Backend service for **Quizapp**, an interactive quiz application with user authentication, configurable quizzes, question management, quiz history, and result tracking.

The backend is implemented as a RESTful API and serves the Android client.

## ✨ Features

- 🔐 User registration and login
- 🔑 JWT-based authentication
- 👤 Authenticated user profile
- 🧠 Quiz question management
- 📚 Category management
- 🎯 Configurable quizzes
- 🖼️ Image and 🔊 audio question support
- 📝 Server-side answer validation
- 📊 Quiz result calculation and history
- 🛡️ Password hashing with bcrypt
- 🚦 Rate limiting for sensitive endpoints
- 🔒 Security middleware and HTTP security headers
- 👨‍💼 Protected admin panel
- 📖 Automatic API documentation with Swagger / ReDoc
- 🗄️ SQLAlchemy database layer
- 🧪 Automated backend tests

## 🏗️ Architecture

```text
Backend
│
├── main.py                 # FastAPI application
├── routers/
│   ├── auth.py
│   ├── categories.py
│   ├── questions.py
│   ├── results.py
│   └── users.py
├── models.py               # SQLAlchemy models
├── schemas.py              # Pydantic schemas
├── crud.py                 # Database operations
├── database.py             # Database configuration
├── auth.py                 # Password hashing & JWT
├── auth_utils.py           # Authentication dependencies
├── security.py             # Security & rate limiting
├── admin.py                # SQLAdmin configuration
├── config.py               # Environment configuration
├── media/
├── scripts/
└── tests/
```

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Backend language |
| **FastAPI** | REST API framework |
| **SQLAlchemy** | ORM / database access |
| **Pydantic** | Data validation |
| **SQLite** | Default database |
| **JWT** | Authentication |
| **bcrypt** | Password hashing |
| **SQLAdmin** | Administration panel |
| **Pytest** | Testing |
| **HTTPX** | API testing |
| **python-dotenv** | Environment configuration |

## 🎮 Quiz Flow

```text
User Login
    │
    ▼
Select Category
    │
    ▼
Select Question Types
(Text / Audio / Image)
    │
    ▼
Select Number of Questions
    │
    ▼
Request Questions
    │
    ▼
Quiz Session
    │
    ▼
Answer Questions
    │
    ▼
Server-side Validation
    │
    ▼
Store History & Result
    │
    ▼
Quiz History
```

The backend controls the quiz session and validates submitted answers instead of trusting the client to determine the correct result.

## 🔐 Authentication

### Register

```http
POST /api/auth/register
```

### Login

```http
POST /api/auth/login
```

A successful login returns a JWT access token:

```json
{
  "access_token": "your-jwt-token",
  "token_type": "bearer"
}
```

Authenticated requests use:

```http
Authorization: Bearer <token>
```

Passwords are hashed using **bcrypt** and are never stored as plain text.

## 📚 API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Register a user |
| `POST` | `/api/auth/login` | Login and receive JWT |

### Users

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/users/me` | Get current user |

### Categories

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/categories/` | Get quiz categories |

### Questions

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/questions/` | Retrieve quiz questions |
| `POST` | `/api/questions/answer` | Validate an answer |

Example:

```http
GET /api/questions/?category=Geography&limit=10
```

### Results

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/results/` | Save quiz result |
| `GET` | `/api/results/` | Get quiz history |

## 🗄️ Data Model

```text
User
 │
 ├── History
 │      └── Question
 │
 └── QuizResult

Category
 │
 └── Question
```

Main entities:

- **User** — account information and password hash
- **Category** — quiz category
- **Question** — question, answers, difficulty, category and media
- **History** — individual answered-question records
- **QuizResult** — completed quiz summary

## 🖼️ Media Support

Quizapp supports:

- 📝 Text questions
- 🖼️ Image questions
- 🔊 Audio questions

Media files are served through:

```text
/media/
```

## 🛡️ Security

The backend includes several security mechanisms:

- bcrypt password hashing
- JWT authentication
- Quiz-session validation
- Rate limiting
- Trusted host middleware
- Configurable CORS
- Security HTTP headers
- `Cache-Control: no-store` for authentication responses
- Environment-based secrets and admin credentials

## 👨‍💼 Admin Panel

The project includes an administration panel powered by **SQLAdmin**.

The admin area can be used to manage application data such as:

- Users
- Categories
- Questions
- Quiz results
- Answer history

```text
/admin
```

Admin credentials are loaded from environment variables.

## 📖 API Documentation

After starting the server:

**Swagger UI**

```text
http://localhost:8000/docs
```

**ReDoc**

```text
http://localhost:8000/redoc
```

## ⚙️ Installation

```bash
git clone <YOUR_BACKEND_REPOSITORY_URL>
cd <BACKEND_DIRECTORY>

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

On Windows:

```powershell
.venv\Scripts\activate
```

## 🔧 Environment Variables

Create a `.env` file:

```env
DATABASE_URL=sqlite:///./quizella.db

SECRET_KEY=your-strong-secret-key

ACCESS_TOKEN_EXPIRE_MINUTES=240

ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-admin-password

CORS_ORIGINS=http://localhost:3000,http://localhost:5173

ALLOWED_HOSTS=localhost,127.0.0.1,10.0.2.2
```

> Never commit `.env` files or production credentials to Git.

## ▶️ Running the Server

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

## 🧪 Testing

Run the test suite with:

```bash
pytest
```

Tests cover areas such as:

- Authentication
- Users
- Questions
- Categories
- Quiz results
- Admin functionality
- Security

## 📱 Android Client

The Android application communicates with this backend using HTTP requests and JWT authentication.

```text
Authentication
      ↓
Categories
      ↓
Questions
      ↓
Answer Validation
      ↓
Quiz Results
      ↓
Quiz History
```

See the companion Android repository for the client implementation.

## 🎓 Project Context

Quizapp was originally based on an existing quiz application frontend and was substantially extended as part of a bachelor's degree project.

The main focus of this work was the design and implementation of the backend, including:

- REST API design
- Authentication and authorization
- Database modeling
- Quiz session management
- Server-side answer validation
- Result and history management
- Media support
- Administration
- Security mechanisms
- Automated testing

## 📄 License

This project is intended as an academic project.

The original Android application was based on the Quizella project by Gautam Hazarika. Please refer to the repository history and included license files for applicable licensing information.
