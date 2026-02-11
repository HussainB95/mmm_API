from sqlalchemy import Column, Integer, String, DateTime #This file is for SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class SpecialInterest(Base):
    __tablename__ = "special_interest"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
