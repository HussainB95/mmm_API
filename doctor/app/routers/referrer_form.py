from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db  # type: ignore
from models import ReferralFormCreate  # type: ignore
from services.referrer_form_services import ReferralFormDB  # type: ignore

router = APIRouter(prefix="/referrer-form", tags=["Referrer Form"])

# View by ID
@router.get("/{id}")
def view_referrer(id: int, db: Session = Depends(get_db)):
    db_referrer = db.query(ReferralFormDB).filter(
        ReferralFormDB.id == id
    ).first()

    if not db_referrer:
        raise HTTPException(status_code=404, detail="Referrer not found")

    return db_referrer


# Create OR Update
@router.post("/create")
def add_or_update_referral(
    id: int,
    data: ReferralFormCreate,
    db: Session = Depends(get_db)
):
    db_referral = (
        db.query(ReferralFormDB)
        .filter(ReferralFormDB.id == id)
        .first()
    )

    if db_referral:
        for key, value in data.model_dump().items():
            setattr(db_referral, key, value)
        db.commit()
        db.refresh(db_referral)
        return {"message": "Referral updated"}

    new_referral = ReferralFormDB(**data.model_dump())
    db.add(new_referral)
    db.commit()
    db.refresh(new_referral)
    return {"message": "Referral created"}


# Delete
@router.delete("/delete/{id}")
def delete_referral(id: int, db: Session = Depends(get_db)):
    obj = db.query(ReferralFormDB).filter(ReferralFormDB.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(obj)
    db.commit()
    return {"message": "Deleted"}
