from sqlalchemy import Column, String, Integer, Enum
from enum import Enum as PyEnum # to prevent name conflict
from .database import Base

class Gender(PyEnum):
    male = "male"
    female = "female"
    other = "other"

class PatientDB(Base):
    __tablename__ = "patient_info"
    
    id = Column(Integer, primary_key= True)
    name = Column(String, nullable=False)
    phone_no = Column(String, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    dob = Column(String, nullable=False)
    blood_group = Column(String)
    profile_image = Column(String)