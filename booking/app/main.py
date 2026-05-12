from fastapi import FastAPI
from .database import engine
from .database_model import Base
from starlette.middleware.sessions import SessionMiddleware
from app.routers.booking_system import router as booking_system_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key = "secret-key") #will change it later

app.include_router(booking_system_router)

@app.get("/")
def home():
    return {"message": "FastAPI running."}