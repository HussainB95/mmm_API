#router\special_interest.py

from fastapi import APIRouter, Depends, FastAPI
from datetime import datetime

from sqlalchemy.orm import Session
from services.special_interest_service import SpecialInterest # type: ignore
from database import session, engine # type: ignore
import database_models # type: ignore

router = APIRouter(prefix="/special-interest", tags=["Special Interest"]) 

database_models.Base. metadata.create_all(bind=engine)

special_interest = [
    SpecialInterest(
        id=1, title="Anxiety"
    ),
    SpecialInterest(
        id=2, title="Depression"
    ),
    SpecialInterest(
        id=3, title="Trauma"
    ),
    SpecialInterest(
        id=4, title="Anger"
    )
]

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
    count = db.query(database_models.SpecialInterest).count

    if count == 0:
        for SpecialInterest in special_interest:
            db.add(database_models.SpecialInterest(**SpecialInterest.model_dump()))
init_db()

#--CRUD--

@router.get("/")
def get_all_special_interest(db: Session = Depends(get_db)):
#def get_all_special_interest():
    db_special_interest = db.query(database_models.SpecialInterest).all()
    # db connection
    #db = session()
    # query
    #db.query()
    #return special_interest
    return db_special_interest

@router.get("/{id}") #prefix already defined, so don't have to write "special-interest" every time
def get_special_interest_by_id(id: int, db: Session = Depends(get_db)):
    db_special_interest = db.query(database_models.SpecialInterest).filter(database_models.SpecialInterest.id == id).first()
    if db_special_interest:
        return db_special_interest
    return "Not Found"
#def get_special_interest_by_id(id: int):
    #return special_interest[id-1]

#create
@router.post("/create")
def create_special_interest(SpecialInterest: SpecialInterest, db: Session = Depends(get_db)):
    db.add(database_models.SpecialInterest(**SpecialInterest.model_dump()))
    db.commit()
    return SpecialInterest

#update
@router.put("/update")
def update_special_interest(id: int, SpecialInterest: SpecialInterest, db: Session = Depends(get_db)):
    db_special_interest = db.query(database_models.SpecialInterest).filter(database_models.SpecialInterest.id == id).first()
    if db_special_interest:
        db_special_interest.title = SpecialInterest.title
        db.commit()
        return "Updated"
    else:
        return "Not Found"
    
#code before data initilization
"""def update_special_interest(id: int, SpecialInterest: SpecialInterest):
    for i in range(len(special_interest)):
        if special_interest[i].id == id:
            special_interest[i] = SpecialInterest
            return "Updated Successfully"
    return {""Not Found""}"""

#delete
@router.delete("/delete") 
def delete_special_interest(id: int, db: Session = Depends(get_db)):
    db_special_interest = db.query(database_models.SpecialInterest).filter(database_models.SpecialInterest.id == id).first()
    if db_special_interest:
        db.delete(db_special_interest)
        db.commit()
        return "Deleted"
    else:
        return {"Not Found"}
    
#code before data initilization
"""@router.delete("/delete") 
def delete_special_interest(id: int):
    for i in range(len(special_interest)):
        if special_interest[i].id == id:
            del special_interest[i]
            return "Deleted"
    return {"Not Found"}"""

