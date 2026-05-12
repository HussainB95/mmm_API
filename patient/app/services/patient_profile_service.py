from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from ..database import get_db
from ..database_table import PatientDB
from ..models import PatientInfo

# Add Patient Profile
def create_profile(data: PatientInfo, db: Session = Depends(get_db)):

    profile = PatientDB(**data.model_dump())

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


# Get Patient Profile
def get_patient(id: id, db: Session = Depends(get_db)):
    patient = db.query(PatientDB).filter(PatientDB.id == id).first()

    return patient


# Update Patient Profile
def update_patient(patient_id: int, profile: PatientInfo, db:Session):
    updated_profile = db.query(PatientDB).filter(PatientDB.id == patient_id).first()

    if not updated_profile:
        raise HTTPException(status_code=404, detail="Not Found")
    
    updated_profile.name = profile.name
    updated_profile.phone_no = profile.phone_no
    updated_profile.gender = profile.gender
    updated_profile.dob = profile.dob
    updated_profile.blood_group = profile.blood_group
    updated_profile.profile_image = profile.profile_image

    db.commit()
    db.refresh(updated_profile)

    return updated_profile
