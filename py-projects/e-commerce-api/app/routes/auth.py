from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, UserLogin, TokenResponse
from app.security import hash_pw, verify_pw, create_access_token, create_email_verification_token, verify_email_token


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
        
        email_token = create_email_verification_token(new_user.id)
        verification_url = (f"http://localhost:8000/auth/verify-email?token={email_token}")
        print(f"Email verification URL: {verification_url}")
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        ) from None

    return new_user

@router.get("/verify-email")
def verify_email(
    token: str,
    db: Annotated[Session, Depends(get_db)],
):
    # 1. Validate token and extract user ID
    user_id = verify_email_token(token)

    # 2. Find the user
    result = db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # 3. Handle an already-verified user
    if user.is_email_verified:
        return {"message": "Email is already verified"}

    # 4. Update verification status
    user.is_email_verified = True
    db.commit()

    return {"message": "Email verified successfully"}

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
