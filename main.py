from fastapi import FastAPI, APIRouter
from patient.app.routers.patient_profile import router as patient_profile_router
from practitioner.app.routers.practitioner_profile import router as practitioner_profile_router
from booking.app.routers.booking_system import router as booking_system_router
from doctor.app.routers.doctor_profile import router as doctor_profile_router
from doctor.app.routers.doctor import router as doctor_router
from doctor.app.routers.referrer_form import router as referrer_form_router
from auth.app.routers.auth import router as auth_router
from admin.app.routers.admin_cms import router as admin_cms_router
from admin.app.routers.kyc_document import router as kyc_document_router
from admin.app.routers.logs import router as logs_router
from admin.app.routers.special_interest import router as special_interest_router
from admin.app.routers.users_manage import router as users_manage_router
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

router = APIRouter(tags=["mmm API"])

app = FastAPI()

Base = declarative_base()

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)

app.include_router(patient_profile_router)
app.include_router(practitioner_profile_router)
app.include_router(booking_system_router)
app.include_router(doctor_profile_router)
app.include_router(doctor_router)
app.include_router(referrer_form_router)
app.include_router(auth_router)
app.include_router(admin_cms_router)
app.include_router(logs_router)
app.include_router(kyc_document_router)
app.include_router(users_manage_router)
app.include_router(special_interest_router)

@app.get("/")
def home():
    return {"message": "Welcome to mmm"}