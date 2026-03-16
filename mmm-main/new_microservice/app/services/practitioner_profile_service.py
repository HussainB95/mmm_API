from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..database_model import PractitionerProfile, VerificationStatus
from ..models import PractitionerProfileCreate, VerificationStatusCreate
from datetime import datetime


# -- CREATE PRACTITIONER PROFILE --

def create_profile(db: Session, data: PractitionerProfileCreate):

    existing = db.query(PractitionerProfile).filter(
        PractitionerProfile.practitioner_id == data.practitioner_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")

    profile = PractitionerProfile(
    id=data.id,
    practitioner_id=data.practitioner_id,
    profile_data=data.profile_data.model_dump(mode="json") if data.profile_data else {},
    banking_details=data.banking_details.model_dump(mode="json") if data.banking_details else {},
    languages=data.languages.model_dump(mode="json") if data.languages else {},
    special_interest=data.special_interest.model_dump(mode="json") if data.special_interest else {},
    modalities=data.modalities.model_dump(mode="json") if data.modalities else {},
    calendar=data.calendar.model_dump(mode="json") if data.calendar else {},
    documents=data.documents.model_dump(mode="json") if data.documents else {},
)
    

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


# -- GET PROFILE --

def get_profile(db: Session, practitioner_id: str):

    profile = db.query(PractitionerProfile).filter(
        PractitionerProfile.practitioner_id == practitioner_id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile



# -- UPDATE SECTION GENERIC --

def update_section(db: Session, practitioner_id: str, column_name: str, value):

    profile = db.query(PractitionerProfile).filter(
        PractitionerProfile.practitioner_id == practitioner_id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    setattr(profile, column_name, value)

    db.commit()
    db.refresh(profile)

    return profile


# -----------------------------
# CREATE VERIFICATION STATUS
# -----------------------------
def create_verification_status(db: Session, data: VerificationStatusCreate):

    verification = VerificationStatus(
        practitioner_id=data.practitioner_id,
        document_name=data.document_name,
        status=data.status,
        verified_at=data.verified_at
    )

    db.add(verification)
    db.commit()
    db.refresh(verification)

    return verification


# -----------------------------
# GET VERIFICATION STATUS
# -----------------------------
def get_verification_status(db: Session, practitioner_id: str):

    return db.query(VerificationStatus).filter(
        VerificationStatus.practitioner_id == practitioner_id
    ).all()


# -- VERIFICATION --

def verify_practitioner_profile(db, practitioner_id, status):

    profile = db.query(PractitionerProfile).filter(
        PractitionerProfile.practitioner_id == practitioner_id
    ).first()

    if not profile:
        raise Exception("Practitioner profile not found")

    profile.verification_status = status
    profile.verified_at = datetime.utcnow()

    db.commit()
    db.refresh(profile)

    return profile


# -- Document Verification --
def verify_document(db, practitioner_id, document_name, status):

    verification = db.query(VerificationStatus).filter(
        VerificationStatus.practitioner_id == practitioner_id,
        VerificationStatus.document_name == document_name
    ).first()

    if not verification:
        verification = VerificationStatus(
            practitioner_id=practitioner_id,
            document_name=document_name,
            status=status,
            verified_at=datetime.utcnow()
        )
        db.add(verification)

    else:
        verification.status = status
        verification.verified_at = datetime.utcnow()

    db.commit()
    db.refresh(verification)

    return verification