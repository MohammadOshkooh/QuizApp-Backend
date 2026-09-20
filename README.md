# Quizella Backend 🎯

Backend service for **Quizella**, an interactive quiz application with user authentication, configurable quizzes, question management, quiz history, and result tracking.

The backend was developed as the main backend component of the project and provides a RESTful API consumed by the Android application.

---

## ✨ Features

- 🔐 User registration and login
- 🔑 JWT-based authentication
- 👤 Authenticated user profile
- 🧠 Quiz question management
- 📚 Category management
- 🎯 Configurable quizzes
- 🖼️ Support for text, image, and audio questions
- 📝 Server-side answer validation
- 📊 Quiz result calculation and history
- 🗃️ Persistent question and quiz history
- 🛡️ Password hashing with bcrypt
- 🚦 Rate limiting for sensitive endpoints
- 🔒 Security middleware and HTTP security headers
- 👨‍💼 Protected admin panel
- 📖 Automatic API documentation with Swagger / ReDoc
- 🗄️ SQLAlchemy-based database layer
- 🧪 Automated backend tests

---

## 🏗️ Architecture

The backend follows a modular structure separating API routing, business logic, database access, authentication, and security concerns.

```text
Backend
│
├── main.py
│   └── FastAPI application and middleware configuration
│
├── routers/
│   ├── auth.py
│   ├── categories.py
│   ├── questions.py
│   ├── results.py
│   └── users.py
│
├── models.py
│   └── SQLAlchemy database models
│
├── schemas.py
│   └── Pydantic request/response schemas
│
├── crud.py
│   └── Database operations
│
├── database.py
│   └── Database configuration and session management
│
├── auth.py
│   └── Password hashing and JWT handling
│
├── auth_utils.py
│   └── Authentication dependencies
│
├── security.py
│   └── Rate limiting and security helpers
│
├── admin.py
│   └── SQLAdmin configuration
│
├── config.py
│   └── Environment-based configuration
│
├── media/
│   ├── images/
│   └── audio/
│
├── scripts/
│   └── Database/content initialization utilities
│
└── tests/
    └── Automated API and security tests
