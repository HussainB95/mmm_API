from sqlalchemy import Column, String, Integer, Float, TIMESTAMP, func, Enum
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum as PyEnum # to prevent name conflict
from .database import Base

class PractitionerProfile(Base):
    __tablename__ = "practitioner_profile"

    id = Column(String, primary_key = True, nullable=False)
    practitioner_id = Column(String, unique=True, nullable=False)

    profile_data = Column(JSONB, nullable=False)
    banking_details = Column(JSONB, nullable=False)
    languages = Column(JSONB, nullable=False)
    special_interest = Column(JSONB, nullable=False)
    modalities = Column(JSONB, nullable=False)
    calendar = Column(JSONB, nullable=False)
    documents = Column(JSONB, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


"""class VerificationStatusEnum(PyEnum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"
    under_review = "Under Review"""


class VerificationStatus(Base):
    __tablename__ = "verification_status"

    id = Column(String, primary_key=True, nullable=False)
    practitioner_id = Column(String, nullable=False)

    document_name = Column(String(100), nullable=False)
    status = Column(String, nullable=False)

    verified_at = Column(TIMESTAMP, nullable=True)    # could be blank


