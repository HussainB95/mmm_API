#router\special_interest.py

from fastapi import APIRouter, Depends, FastAPI
from datetime import datetime
from sqlalchemy.orm import Session
from services.special_interest_service import SpecialInterest # type: ignore
from database import session, engine # type: ignore
import models

router = APIRouter(prefix="/special-interest", tags=["Special Interest"]) 

models.Base. metadata.create_all(bind=engine)

#Closing the connection after use

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()  

#Initialization of data

def init_db():
    db = session()
    count = db.query(models.SpecialInterest).count

    if count == 0:
        for SpecialInterest in SpecialInterest:
            db.add(models.SpecialInterest(**SpecialInterest.model_dump()))
init_db()

#--CRUD--

@router.get("/")
def get_all_special_interest(db: Session = Depends(get_db)):
    db_special_interest = db.query(models.SpecialInterest).all()
    return db_special_interest

@router.get("/{id}") #prefix already defined, so don't have to write "special-interest" every time
def get_special_interest_by_id(id: int, db: Session = Depends(get_db)):
    db_special_interest = db.query(models.SpecialInterest).filter(models.SpecialInterest.id == id).first()
    if db_special_interest:
        return db_special_interest
    return "Not Found"

#create
@router.post("/create")
def create_special_interest(SpecialInterest: SpecialInterest, db: Session = Depends(get_db)):
    db.add(models.SpecialInterest(**SpecialInterest.model_dump()))
    db.commit()
    return SpecialInterest

#update
@router.put("/update")
def update_special_interest(id: int, SpecialInterest: SpecialInterest, db: Session = Depends(get_db)):
    db_special_interest = db.query(models.SpecialInterest).filter(models.SpecialInterest.id == id).first()
    if db_special_interest:
        db_special_interest.title = SpecialInterest.title
        db.commit()
        return "Updated"
    else:
        return "Not Found"

#delete
@router.delete("/delete") 
def delete_special_interest(id: int, db: Session = Depends(get_db)):
    db_special_interest = db.query(models.SpecialInterest).filter(models.SpecialInterest.id == id).first()
    if db_special_interest:
        db.delete(db_special_interest)
        db.commit()
        return "Deleted"
    else:
        return {"Not Found"}

