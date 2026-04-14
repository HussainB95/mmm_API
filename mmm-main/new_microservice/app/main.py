from fastapi import FastAPI
from .database import engine
from .database_model import Base
from starlette.middleware.sessions import SessionMiddleware
from app.routers.practitioner_profile import router as practitioner_profile_router # type: ignore

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key = "secret-key" #will change it later
)

app.include_router(practitioner_profile_router)