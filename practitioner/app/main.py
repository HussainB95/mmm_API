from fastapi import FastAPI
from .database import engine
from .database_table import Base
from starlette.middleware.sessions import SessionMiddleware
from routers.practitioner_profile import router as practitioner_profile_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key = "secret-key" #will change it later
)

app.include_router(practitioner_profile_router)

@app.get("/")
def home():
    return {"message": "FastAPI running."}