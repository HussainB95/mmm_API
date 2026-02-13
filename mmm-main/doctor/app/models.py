from pydantic import BaseModel
from typing import Optional, Literal

class ReferralFormCreate(BaseModel):
    doctor_id: str
    patient_id: str
    therapist_id: str
    urgency: Literal["Low", "Medium", "High", "Emergency"]
    modality: Literal["Therapy", "Psychiatric Assessment", "Both"]
    clinical_presentation: str
    chief_complaint: str
    additional_requirements: Optional[str] = None

class ReferralFormOut(ReferralFormCreate):
    id: int

    class Config:
        from_attributes = True


# -- Doctor --

class UserRole(BaseModel):
    role: Literal["patient", "therapist"]

class DoctorProfileCreate(BaseModel):
    doctor_id: str
    full_name: str
    license_number: str
    registration: str
    clinic_name: Optional[str] = None
    medical_field: str
    address: str
    phone: str
    gender: Literal["male", "female", "other"]
    dob: str
