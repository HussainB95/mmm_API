from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import uuid
from datetime import datetime

db_url = "postgresql://postgres:Myp0stgre$@localhost:5432/mmm"

Base = declarative_base()

engine = create_engine(db_url)

SessionLocal = sessionmaker(bind = engine) 

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=True)
    role = Column(String, default="patient")
    name = Column(String)
    phone = Column(String)

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
    magic_token = Column(String, nullable=True)
    magic_token_expiry = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    is_verified = Column(Boolean, default=False)
    email_verification_token = Column(String, nullable=True)
    email_verification_expiry = Column(DateTime, nullable=True)

    reset_password_token = Column(String, nullable=True)
    reset_password_expiry = Column(DateTime, nullable=True)