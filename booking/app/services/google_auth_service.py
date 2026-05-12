from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database_model import GoogleAuth


def get_google_auth_by_user_id(db, user_id: int):
    return db.query(GoogleAuth).filter(GoogleAuth.user_id == user_id).first()


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