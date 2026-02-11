from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
from database_models import Base, SpecialInterestDB
from models import SpecialInterestCreate, SpecialInterestOut

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MMM Admin API") #object created

origins = [
    "https://auto-parts-front.vercel.app",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "MMM Admin API running"}

#CRUD
@app.get("/special-interest", response_model=list[SpecialInterestOut])
def get_all(db: Session = Depends(get_db)):
    return db.query(SpecialInterestDB).all()

@app.post("/special-interest", response_model=SpecialInterestOut)
def create(data: SpecialInterestCreate, db: Session = Depends(get_db)):
    obj = SpecialInterestDB(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.put("/special-interest/{id}")
def update(id: int, data: SpecialInterestCreate, db: Session = Depends(get_db)):
    obj = db.query(SpecialInterestDB).filter(SpecialInterestDB.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not Found")

    for k, v in data.dict().items():
        setattr(obj, k, v)

    db.commit()
    return {"message": "Updated successfully"}

@app.delete("/special-interest/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    obj = db.query(SpecialInterestDB).filter(SpecialInterestDB.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not Found")

    db.delete(obj)
    db.commit()
    return {"message": "Deleted successfully"}
