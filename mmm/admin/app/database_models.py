from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class SpecialInterestDB(Base):
    __tablename__ = "special_interest"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    content = Column(String)
    thumbnail = Column(String)
    status = Column(String, default="draft")
    meta_title = Column(String)
    meta_description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
