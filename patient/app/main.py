from fastapi import FastAPI
from .database import engine
from .database_table import Base
from starlette.middleware.sessions import SessionMiddleware
from app.routers.patient_profile import router as patient_profile_router # type: ignore

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key = "secret-key" #will change it later
)

app.include_router(patient_profile_router)

@app.get("/")
def home():
    return {"message": "FastAPI running."}