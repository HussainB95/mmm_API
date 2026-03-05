from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from ..models import (MagicUserLogin, UserRegister, UserOut, UserLogin, ForgotPasswordRequest, ResetPasswordRequest)
from ..database import get_db
from ..services import auth_service

router = APIRouter()

@router.post("/register")
def register(
    data: UserRegister,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    return auth_service.register_user(db, data, background_tasks)


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    return auth_service.verify_email_token(db, token)

# User login
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    return auth_service.login_user(db, data)

# Forgot password
@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    return auth_service.forgot_password_service(db, data, background_tasks)


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    return auth_service.reset_password_service(db, data)


# User magiclogin
@router.post("/magiclogin")
def magic_login(
    data: MagicUserLogin,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    return auth_service.magic_login_service(db, data, background_tasks)


@router.get("/verify-magiclogin")
def verify_magic(token: str, db: Session = Depends(get_db)):
    return auth_service.verify_magic_service(db, token)