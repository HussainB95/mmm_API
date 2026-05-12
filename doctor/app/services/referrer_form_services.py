from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

class Urgency(str, enum.Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"
    Emergency = "Emergency"

class Modality(str, enum.Enum):
    Therapy = "Therapy"
    Psychiatric = "Psychiatric Assessment"
    Both = "Both"

class ReferralFormDB(Base):
    __tablename__ = "referrer_form"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(String, nullable=False)
    patient_id = Column(String, nullable=False)
    therapist_id = Column(String, nullable=False)
    urgency = Column(Enum(Urgency), nullable=False)
    modality = Column(Enum(Modality), nullable=False)
    clinical_presentation = Column(String, nullable=False)
    chief_complaint = Column(String, nullable=False)
    additional_requirements = Column(String)
