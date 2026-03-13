from fastapi import FastAPI
from .database import engine
from .database_model import Base
from app.routers.practitioner_profile import router as practitioner_profile_router # type: ignore

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(practitioner_profile_router)