#routers\doctor_profile.py

from fastapi import FastAPI,APIRouter, HTTPException, Request, Depends
from models import UserRole, DoctorProfileCreate # type: ignore
from uuid import UUID
from services.doctor_profile_services import Base, DoctorProfileDB  # type: ignore
from database import get_db, Session # type: ignore
import models # type: ignore

router = APIRouter(prefix="/doctor-profile", tags=["Doctor Profile"])

@router.get("/{doctor_id}")
async def view_doctor(doctor_id: str, db: Session = Depends(get_db)):
    db_profile = db.query(DoctorProfileDB).filter(DoctorProfileDB.doctor_id == doctor_id).first()
    
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return db_profile


@router.post("/create")
async def add_or_update_profile(
    profile: DoctorProfileCreate,
    db: Session = Depends(get_db)
):
    # Check if doctor already exists
    db_profile = db.query(DoctorProfileDB).filter(DoctorProfileDB.doctor_id == profile.doctor_id).first()

    if db_profile:
        # Update existing profile
        for key, value in profile.dict().items():
            setattr(db_profile, key, value)

        db.commit()
        db.refresh(db_profile)
        return {"message": "Profile updated"}

    else:
        # Create new profile
        new_profile = DoctorProfileDB(**profile.dict())
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return {"message": "Profile created"}


