#router\special_interest.py

from fastapi import APIRouter
from datetime import datetime
from services.special_interest_service import SpecialInterest # type: ignore
from database import session, engine # type: ignore
import database_models # type: ignore

router = APIRouter(prefix="/special-interest", tags=["Special Interest"]) 

database_models.Base. metadata.create_all(bind=engine)

special_interest = [
    SpecialInterest(
        id=1, slug="anxiety", title="Anxiety",
        content="content", thumbnail="thumbnail", status="Active",
        created_at=datetime.now(), updated_at=datetime.now()
    ),
    SpecialInterest(
        id=2, slug="depression", title="Depression",
        content="content", thumbnail="thumbnail", status="Active",
        created_at=datetime.now(), updated_at=datetime.now()
    ),
    SpecialInterest(
        id=3, slug="Trauma", title="Trauma",
        content="content", thumbnail="thumbnail", status="Active",
        created_at=datetime.now(), updated_at=datetime.now()
    ),
    SpecialInterest(
        id=4, slug="Anger", title="Anger",
        content="content", thumbnail="thumbnail", status="Inactive",
        created_at=datetime.now(), updated_at=datetime.now()
    ),
]

#--CRUD--

@router.get("/")
def get_all_special_interest():
    # db connection
    #db = session()
    # query
    #db.query()
    return special_interest

@router.get("/{id}") #prefix already defined, so don't have to write "special-interest" every time
def get_special_interest_by_id(id: int):
    return special_interest[id-1]

@router.post("/create") #create
def create_special_interest(SpecialInterest: SpecialInterest):
    special_interest.append(SpecialInterest)
    return SpecialInterest

@router.put("/update") #update
def update_special_interest(id: int, SpecialInterest: SpecialInterest):
    for i in range(len(special_interest)):
        if special_interest[i].id == id:
            special_interest[i] = SpecialInterest
            return "Updated Successfully"
    return "Not Found"

@router.delete("/delete") #delete
def delete_special_interest(id: int):
    for i in range(len(special_interest)):
        if special_interest[i].id == id:
            del special_interest[i]
            return "Deleted"
    return "Not Found"

