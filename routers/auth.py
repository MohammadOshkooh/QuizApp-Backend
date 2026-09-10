from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth import (
    create_access_token,
    verify_password
)
from crud import (
    create_user,
    get_user
)
from database import get_db
from schemas import (
    Token,
    UserCreate,
    UserLogin,
    UserOut
)
from security import (
    get_client_ip,
    login_rate_limiter,
    register_rate_limiter
)


router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
def register(
    user: UserCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    client_ip = get_client_ip(request)

    register_rate_limiter.check(
        f"register:{client_ip}"
    )

    existing_user = get_user(
        db,
        user.username
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists."
        )

    try:
        return create_user(
            db,
            user
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists."
        )


@router.post(
    "/login",
    response_model=Token
)
def login(
    user: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    client_ip = get_client_ip(request)

    login_rate_limiter.check(
        f"login:{client_ip}"
    )

    db_user = get_user(
        db,
        user.username
    )

    if (
        not db_user
        or not verify_password(
            user.password,
            db_user.hashed_password
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    token = create_access_token(
        user_id=db_user.id
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }