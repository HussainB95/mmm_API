from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime, date
import uuid

# -- GoogleOAth --

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    picture: Optional[str] = None

class UserCreate(BaseModel):
    google_id: str

class UserResponse(UserBase):
    id: uuid.UUID
    google_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# -- PractitionerProfile --

class Oauth(BaseModel):
    id: str
    email: str
    password: str

class ProfileData(BaseModel):
    name: str
    qualifications: str
    license_number: str

class BankingDetails(BaseModel):
    beneficiary_name: str
    bank_name: str
    account_num: int
    branch_num: str

class Languages(BaseModel):
    languages: list[str]

class SpecialInterest(BaseModel):
    specialinterest: list[str]

class Modalities(BaseModel):
    modalities: list[str]

class Calendar(BaseModel):
    availability: Dict[str, list[str]]

class DocumentItem(BaseModel):
    file_url: str
    expiry_date: Optional[date] = None

class Documents(BaseModel):
    hpcsa_sacss: DocumentItem
    bhf: Optional[DocumentItem] = None
    mps: Optional[DocumentItem] = None
    cpd: Optional[DocumentItem] = None

class Gender(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class ProfileImage(BaseModel):
    file_url: str

class PatientInfo(BaseModel):
    name: str
    phone_no: int
    gender: Gender
    dob: str
    blood_group: str
    profile_image: ProfileImage

class PractitionerProfileBase(BaseModel):
    id: str  
    practitioner_id: str

    profile_data: Optional[ProfileData] = None
    patient_info: Optional[PatientInfo] = None
    banking_details: Optional[BankingDetails] = None
    languages: Optional[Languages] = None
    special_interest: Optional[SpecialInterest] = None
    modalities: Optional[Modalities] = None
    calendar: Optional[Calendar] = None
    documents: Optional[Documents] = None


class PractitionerProfileCreate(PractitionerProfileBase): # it will take required fields form PractitionerProfileBase    when needed.
    pass

class PractitionerProfileResponse(PractitionerProfileBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# -- VerificationStatus --
class VerificationStatusEnum(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    under_review = "under_review"

class DocumentEnum(str, Enum):
    hpcsa_sacss = "hpcsa_sacss"
    bhf = "bhf"
    mps = "mps"
    cpd = "cpd"

class VerificationStatusBase(BaseModel):
    practitioner_id: str
    document_name: DocumentEnum
    status: VerificationStatusEnum # used Enum for the fixed inputs
    verified_at: Optional[datetime] = None

class VerificationStatusCreate(VerificationStatusBase):
    pass

class VerificationStatusResponse(VerificationStatusBase):
    id: str

    class Config:
        orm_mode = True