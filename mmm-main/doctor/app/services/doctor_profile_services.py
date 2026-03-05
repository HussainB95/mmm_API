#routers\doctor_profile_services.py

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Date, String

Base = declarative_base()

class DoctorProfileDB(Base):
    __tablename__ = "doctor_profile"
    
    doctor_id = Column(String, primary_key = True, nullable = False)
    full_name = Column(String, nullable = False)
    license_number = Column(String, unique=True, nullable = False)
    registration = Column(String, nullable = False)
    clinic_name = Column(String)
    medical_field = Column(String, nullable = True)
    address = Column(String, nullable = False)
    phone = Column(String, nullable = False)
    gender = Column(String["male", "female", "other"])
    dob = Column(Date, nullable = False)