from os import name
import uuid
from datetime import datetime, timedelta
from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from ..database_model import User
from ..security import hash_password, verify_password, create_access_token
from .email_service import send_email # type: ignore


# ==============================
# REGISTER USER
# ==============================
def register_user(db: Session, data, background_tasks: BackgroundTasks):

    # Check if email already exists
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Create user
    user = User(
        email=data.email,
        password=hash_password(data.password),
        role=data.role,
        name=data.name,
        phone=data.phone,
        is_verified=False,
    )

    # Generate verification token
    token = str(uuid.uuid4())
    user.email_verification_token = token
    user.email_verification_expiry = datetime.utcnow() + timedelta(hours=24)

    db.add(user)
    db.commit()
    db.refresh(user)

    # Send verification email in background
    verification_link = f"http://localhost:8000/auth/verify-email?token={token}"

    background_tasks.add_task(
        send_email,
        user.email,
        "Verify Your Email",
        f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px;">
                
                <h2 style="color: #333;">Verify Your Email Address</h2>
                
                <p>Hi,</p>
                
                <p>Thank you for registering with us.</p>
                
                <p>Please click the button below to verify your email address:</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_link}" 
                       style="background-color: #4CAF50; 
                              color: white; 
                              padding: 12px 25px; 
                              text-decoration: none; 
                              border-radius: 5px;
                              font-weight: bold;">
                        Verify Email
                    </a>
                </div>
                
                <p>This link will expire in <strong>30 minutes</strong>.</p>
                
                <p>If you did not create this account, you can safely ignore this email.</p>
                
                <hr>
                
                <p style="font-size: 12px; color: gray;">
                    If the button doesn't work, copy and paste this link into your browser:
                    <br>
                    {verification_link}
                </p>
                
                <p>Best regards,<br>mmm Team</p>
            
            </div>
        </body>
    </html>
    """
    )

    return user


# ==============================
# VERIFY EMAIL
# ==============================
def verify_email_token(db: Session, token: str):

    user = db.query(User).filter(
        User.email_verification_token == token
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    if user.email_verification_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    user.is_verified = True
    user.email_verification_token = None
    user.email_verification_expiry = None

    db.commit()

    return {"message": "Email verified successfully"}


# ==============================
# LOGIN USER
# ==============================
def login_user(db: Session, data):

    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Email not verified")

    access_token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==============================
# FORGOT PASSWORD
# ==============================
def forgot_password_service(db: Session, data, background_tasks: BackgroundTasks):

    user = db.query(User).filter(User.email == data.email).first()

    # Security best practice:
    # Don't reveal whether email exists
    if not user:
        return {"message": "If email exists, reset link sent"}

    token = str(uuid.uuid4())
    user.reset_password_token = token
    user.reset_password_expiry = datetime.utcnow() + timedelta(hours=1)

    db.commit()

    reset_link = f"http://localhost:8000/auth/reset-password?token={token}"

    background_tasks.add_task(
        send_email,
        user.email,
        "Reset Password",
        f"""
        <h3>Password Reset</h3>
        <p>Click below link to reset your password:</p>
        <a href="{reset_link}">Reset Password</a>
        """
    )

    return {"message": "If email exists, reset link sent"}


# ==============================
# RESET PASSWORD
# ==============================
def reset_password_service(db: Session, data):

    user = db.query(User).filter(
        User.reset_password_token == data.token
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    if user.reset_password_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    user.password = hash_password(data.new_password)
    user.reset_password_token = None
    user.reset_password_expiry = None

    db.commit()

    return {"message": "Password reset successful"}


# ==============================
# MAGIC LOGIN
# ==============================
def magic_login_service(db: Session, data, background_tasks: BackgroundTasks):

    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = str(uuid.uuid4())
    user.magic_token = token
    user.magic_token_expiry = datetime.utcnow() + timedelta(minutes=10)

    db.commit()

    magic_link = f"http://localhost:8000/auth/verify-magiclogin?token={token}"

    background_tasks.add_task(
        send_email,
        user.email,
        "Magic Login",
        f"""
        <h3>Magic Login</h3>
        <p>Click below to login instantly:</p>
        <a href="{magic_link}">Login Now</a>
        """
    )

    return {"message": "Magic login link sent"}


# ==============================
# VERIFY MAGIC LOGIN
# ==============================
def verify_magic_service(db: Session, token: str):

    user = db.query(User).filter(User.magic_token == token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    if user.magic_token_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    user.magic_token = None
    user.magic_token_expiry = None

    db.commit()

    access_token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }