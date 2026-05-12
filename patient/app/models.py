from enum import Enum
from pydantic import BaseModel

class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class ProfileImage(BaseModel):
    file_url: str

class PatientInfo(BaseModel):
    name: str
    phone_no: str
    gender: Gender
    dob: str
    blood_group: str
    profile_image: str

class PatientInfoResponse(PatientInfo):
    id: int

    class Config:
        from_attributes = True