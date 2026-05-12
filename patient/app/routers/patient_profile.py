from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import PatientInfoResponse, PatientInfo
from ..services import patient_profile_service

app = FastAPI()

router = APIRouter(prefix="/patients", tags=["Patient Profile"])

app.include_router(router)

# Add Patient Profile
@router.post("/", response_model=PatientInfoResponse)
def create_profile(data: PatientInfo, db: Session = Depends(get_db)):

    return patient_profile_service.create_profile(data, db)

# Get Patient Profile
@router.get("/{patient_id}", response_model=PatientInfoResponse)
def get_patient(id: int, db: Session = Depends(get_db)):
    return patient_profile_service.get_patient(id, db)

# Update Patient Profile
@router.put("/{patient_id}", response_model=PatientInfoResponse)
def update_patient(patient_id: int, profile: PatientInfo, db:Session = Depends(get_db)):

    return patient_profile_service.update_patient(patient_id,profile, db)