from sqlalchemy import Column, String, Integer, Float, TIMESTAMP, func, Enum
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum as PyEnum # to prevent name conflict
from .database import Base
import uuid


class VerificationStatusEnum(PyEnum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    under_review = "under_review"
    
class PractitionerProfile(Base):
    __tablename__ = "practitioner_profile"

    id = Column(String, primary_key=True, nullable=False)
    practitioner_id = Column(String, unique=True, nullable=False)

    profile_data = Column(JSONB, nullable=False)
    banking_details = Column(JSONB, nullable=False)
    languages = Column(JSONB, nullable=False)
    special_interest = Column(JSONB, nullable=False)
    modalities = Column(JSONB, nullable=False)
    calendar = Column(JSONB, nullable=False)
    documents = Column(JSONB, nullable=False)

    # edded this for verification later
    verification_status = Column(
        Enum(VerificationStatusEnum),
        default=VerificationStatusEnum.pending
    )

    verified_at = Column(TIMESTAMP, nullable=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


class DocumentEnum(PyEnum):
    hpcsa_sacss = "hpcsa_sacss"
    bhf = "bhf"
    mps = "mps"
    cpd = "cpd"

class VerificationStatus(Base):
    __tablename__ = "verification_status"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    practitioner_id = Column(String, nullable=False)

    document_name = Column(Enum(DocumentEnum), nullable=False)
    status = Column(Enum(VerificationStatusEnum), nullable=False)

    verified_at = Column(TIMESTAMP, nullable=True) # could be blank


