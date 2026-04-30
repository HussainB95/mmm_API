from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session
from ..services import practitioner_profile_service
from ..database import get_db
from ..models import (PractitionerProfileResponse, PractitionerProfileCreate, ProfileData,
                      Languages, PatientInfo, BankingDetails, VerificationStatusCreate,
                      Documents, SpecialInterest, Modalities, Calendar)

app = FastAPI()

router = APIRouter(prefix="/practitioner", tags=["Practitioner Profile"])

app.include_router(router)

@router.post("/create", response_model=PractitionerProfileResponse)
def create_profile(
    data: PractitionerProfileCreate,
    db: Session = Depends(get_db)
):
    return practitioner_profile_service.create_profile(db, data)


@router.get("/{practitioner_id}", response_model=PractitionerProfileResponse)
def get_profile(
    practitioner_id: str,
    db: Session = Depends(get_db)
):
    return practitioner_profile_service.get_profile(db, practitioner_id)


@router.put("/personal-info/{practitioner_id}")
def update_personal_info(
    practitioner_id: str,
    data: ProfileData,
    db: Session = Depends(get_db)
):
    return practitioner_profile_service.update_section(
        db,
        practitioner_id,
        "profile_data",
        data.model_dump()
    )


@router.put("/patient-info/{practitioner_id}")
def update_patient_info(
    practitioner_id: str,
    data: PatientInfo,
    db: Session = Depends(get_db)
):
    return practitioner_profile_service.update_section(
        db,
        practitioner_id,
        "patient_info",
        data.model_dump()
    )


@router.put("/banking/{practitioner_id}")
def update_banking(
    practitioner_id: str,
    data: BankingDetails,
    db: Session = Depends(get_db)
):
    return practitioner_profile_service.update_section(
        db,
        practitioner_id,
        "banking_details",
        data.model_dump()
    )


@router.put("/languages/{practitioner_id}")
def update_languages(
    practitioner_id: str,
    data: Languages,
    db: Session = Depends(get_db)
):
    return practitioner_profile_service.update_section(
        db,
        practitioner_id,
        "languages",
        data.model_dump()
    )


@router.put("/special-interest/{practitioner_id}")
def update_special_interest(
    practitioner_id: str,
    data: SpecialInterest,
    db: Session = Depends(get_db)
):
    return practitioner_profile_service.update_section(
        db,
        practitioner_id,
        "special_interest",
        data.model_dump()
    )


@router.put("/modalities/{practitioner_id}")
def update_modalities(
    practitioner_id: str,
    data: Modalities,
    db: Session = Depends(get_db)
):
    return practitioner_profile_service.update_section(
        db,
        practitioner_id,
        "modalities",
        data.model_dump()
    )


@router.put("/calendar/{practitioner_id}")
def update_calendar(
    practitioner_id: str,
    data: Calendar,
    db: Session = Depends(get_db)
):
    return practitioner_profile_service.update_section(
        db,
        practitioner_id,
        "calendar",
        data.model_dump()
    )


@router.put("/documents/{practitioner_id}")
def update_documents(
    practitioner_id: str,
    data: Documents,
    db: Session = Depends(get_db)
):
    return practitioner_profile_service.update_section(
        db,
        practitioner_id,
        "documents",
        data.model_dump(mode="json")
    )


@router.patch("/verification/{practitioner_id}")
def update_verification(
    practitioner_id: str,
    data: VerificationStatusCreate,
    db: Session = Depends(get_db)
):
    profile = practitioner_profile_service.verify_practitioner_profile(
        db,
        practitioner_id,
        data.status
    )

    if not profile:
        raise HTTPException(status_code=404, detail="Practitioner not found")

    return {
        "message": "Verification status updated",
        "status": profile.verification_status
    }
