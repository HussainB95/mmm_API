from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db # type: ignore
from models import ReferralFormCreate, ReferralFormOut # type: ignore
from services.referrer_form_services import ReferralFormDB # type: ignore

router = APIRouter(prefix="/referrer-form", tags=["Referrer Form"])

# -- CRUD --

@router.get("/")
def get_all_referral(db: Session = Depends(get_db)):
    return db.query(ReferralFormDB).all()

@router.get("/{id}")
def get_referral_by_id(id: int, db: Session = Depends(get_db)):
    obj = db.query(ReferralFormDB).filter(ReferralFormDB.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.post("/create")
def create_referral(data: ReferralFormCreate, db: Session = Depends(get_db)):
    obj = ReferralFormDB(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.put("/update/{id}")
def update_referral(id: int, data: ReferralFormCreate, db: Session = Depends(get_db)):
    obj = db.query(ReferralFormDB).filter(ReferralFormDB.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")

    for key, value in data.model_dump().items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/delete/{id}")
def delete_referral(id: int, db: Session = Depends(get_db)):
    obj = db.query(ReferralFormDB).filter(ReferralFormDB.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(obj)
    db.commit()
    return {"message": "Deleted"}
