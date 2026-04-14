from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database_model import GoogleAuth, User
from fastapi import Request, HTTPException
from dotenv import load_dotenv
from jose import jwt
import httpx
from ..auth import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, GOOGLE_AUTH_ENDPOINT, GOOGLE_USERINFO_ENDPOINT, GOOGLE_TOKEN_ENDPOINT

def save_google_auth(
        db:Session,
        user_id:int,
        google_id:str,
        access_token: str,
        refresh_token: str,
        expires_in: int
):
    token_expiry = datetime.utcnow() + timedelta(seconds=expires_in)

    existing = db.query(GoogleAuth).filter(GoogleAuth.google_id == google_id).first()

    if existing:
        existing.access_token = access_token
        if refresh_token:
            existing.refresh_token = refresh_token
        existing.token_expiry = token_expiry

    else:
        new_auth = GoogleAuth(
            user_id=user_id,
            google_id=google_id,
            access_token=access_token,
            refresh_token=refresh_token,
            token_expiry=token_expiry
        )
        db.add(new_auth)
    db.commit()