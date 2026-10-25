from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, UserLogin, TokenResponse
from app.security import hash_pw, verify_pw, create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

DbSession = Annotated[Session, Depends(get_db)]

@router.get("/health")
def auth_health():
    return {"message": "Auth router is working"}

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: DbSession):
    existing_user = db.scalar(
        select(User).where(User.email == str(user_data.email))
    )
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists"
        )
        
    new_user = User(
        email = str(user_data.email),
        password_hash = hash_pw(user_data.password)
    )
    
    db.add(new_user)
    
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        ) from None

    return new_user

@router.post("/login", response_model=TokenResponse)
def login_user(user_data: UserLogin, db: DbSession):
    user = db.scalar(
        select(User).where(User.email == str(user_data.email))
    )

    # Use the same error for unknown email and wrong password
    if user is None or not verify_pw(
        user_data.password, user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is inactive",
        )

    if not user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in",
        )

    token = create_access_token(user.id)

    return TokenResponse(access_token=token)
