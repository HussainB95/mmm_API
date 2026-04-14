from fastapi import APIRouter, Depends, HTTPException, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from ..services import practitioner_profile_service
from ..database import get_db
from ..models import *
from ..database_model import PractitionerProfile, User
from dotenv import load_dotenv
from ..auth import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, GOOGLE_AUTH_ENDPOINT, GOOGLE_USERINFO_ENDPOINT, GOOGLE_TOKEN_ENDPOINT
from urllib.parse import urlencode
import httpx
from jose import jwt
from app.services.google_auth_service import save_google_auth

app = FastAPI()
router = APIRouter(tags=["Practitioner Profile"])

app.add_middleware(SessionMiddleware, secret_key = "secret-key")

#Google oath
@router.get("/home", response_class=HTMLResponse)
async def hello():
    return """
    <h2>Welcome to mmm Login</h2>
    <a href = "/login">Login with Google</a>
    """

#Google oath login
@router.get("/login")
async def login():
    query_params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    
    url = f"{GOOGLE_AUTH_ENDPOINT}?{urlencode(query_params)}"
    return RedirectResponse(url)

#Google oath callback
@router.get("/google/callback")
async def auth_callback(request: Request, db:Session = Depends(get_db)):
    code = request.query_params.get("code")

    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")
    
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(GOOGLE_TOKEN_ENDPOINT, data = data)
        token_data = token_response.json()

        #fetching data
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        id_token = token_data.get("id_token")
        expires_in = token_data.get("expires_in")


        if not access_token or not id_token:
            raise HTTPException(status_code=400, detail="Failed to retrieve access token")
        
        #decoding id_token
        user_data = jwt.get_unverified_claims(id_token)

        google_id = user_data.get("sub")
        email = user_data.get("email")
        name = user_data.get("name")
        picture = user_data.get("picture")

        user = db.query(User).filter(User.google_id == google_id).first()

        if not user:
            user = User(
                email = email,
                name = name,
                google_id = google_id,
                picture = user_data.get("picture")
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        #fetching use
        user_id = user.id

        request.session["user"] = {
            "id": str(user.id),
            "email": email,
            "name": name,
            "picture": user_data.get("picture")
        }

        #saving data(Token) in db
        save_google_auth(
            db=db,
            user_id=user_id,
            google_id=google_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in
        )

        return RedirectResponse("/profile")


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    user_info = request.session.get("user")

    if not user_info:
        return RedirectResponse("/home")
    
    return f"""
    <html>
        <head><title>User Profile</title></head>
        <body style="text-align:center; font-family: sans-serif;">
        <h1>Welcome, {user_info['name']}!</h1>
        <img src="{user_info['picture']}" alt="Profile Picture" width="120"/><br>
        <p>Email: {user_info['email']}</p>    
        </body>
    </html> 
"""

# Logout
@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/home")


app.include_router(router)

@router.post("/create_profile", response_model=PractitionerProfileResponse)
def create_profile(data: PractitionerProfileCreate, db: Session = Depends(get_db)):
    return practitioner_profile_service.create_profile(db, data)

@router.get("/{practitioner_id}", response_model=PractitionerProfileResponse)
def get_profile(practitioner_id: str, db: Session = Depends(get_db)):
    return practitioner_profile_service.get_profile(db, practitioner_id)

@router.put("/personal-info/{practitioner_id}")
def update_personal_info(practitioner_id: str, data: ProfileData, db: Session = Depends(get_db)):
    return practitioner_profile_service.update_section(
        db,
        practitioner_id,
        "profile_data",
        data.model_dump()
    )

@router.put("/patient-info/{practitioner_id}")
def update_patient_info(practitioner_id: str, data: PatientInfo, db: Session = Depends(get_db)):
    return practitioner_profile_service.update_section(
        db,
        practitioner_id,
        "patient_info",
        data.model_dump()
    )

@router.put("/banking/{practitioner_id}")
def update_banking(practitioner_id: str, data: BankingDetails, db: Session = Depends(get_db)):
    return practitioner_profile_service.update_section(
        db,
        practitioner_id,
        "banking_details",
        data.model_dump()
    )

@router.put("/languages/{practitioner_id}")
def update_languages(practitioner_id: str, data: Languages, db: Session = Depends(get_db)):
    return practitioner_profile_service.update_section(
        db,
        practitioner_id,
        "languages",
        data.model_dump()
    )

@router.put("/special-interest/{practitioner_id}")
def update_special_interest(practitioner_id: str, data: SpecialInterest, db: Session = Depends(get_db)):
    return practitioner_profile_service.update_section(
        db,
        practitioner_id,
        "special_interest",
        data.model_dump()
    )

@router.put("/modalities/{practitioner_id}")
def update_modalities(practitioner_id: str, data: Modalities, db: Session = Depends(get_db)):
    return practitioner_profile_service.update_section(
        db,
        practitioner_id,
        "modalities",
        data.model_dump()
    )

@router.put("/calendar/{practitioner_id}")
def update_calendar(practitioner_id: str, data: Calendar, db: Session = Depends(get_db)):
    return practitioner_profile_service.update_section(
        db,
        practitioner_id,
        "calendar",
        data.model_dump()
    )

@router.put("/documents/{practitioner_id}")
def update_documents(practitioner_id: str, data: Documents, db: Session = Depends(get_db)):
    return practitioner_profile_service.update_section(
        db,
        practitioner_id,
        "documents",
        data.model_dump(mode="json")
    )

@router.patch("/verification/{practitioner_id}")
def update_verification(
    practitioner_id: str,
    data: VerificationStatusCreate,
    db: Session = Depends(get_db)
):

    profile = practitioner_profile_service.verify_practitioner_profile(
        db,
        practitioner_id,
        data.status
    )

    if not profile:
        raise HTTPException(status_code=404, detail="Practitioner not found")

    return {
        "message": "Verification status updated",
        "status": profile.verification_status
    }