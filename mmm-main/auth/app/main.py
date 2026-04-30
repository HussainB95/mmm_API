from collections import deque
import threading
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router # type: ignore
from app.database_model import engine, Base # type: ignore

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include router
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

origins = [
    "https://auto-parts-front.vercel.app",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# -------------------
# Rate Limiter
# -------------------

lock = threading.Lock()
REQUEST_LOG = {}
BLOCKED_IPS = {}

LIMIT = 1000
WINDOW = 60
BLOCK_DURATION = 120


@app.middleware("http")
async def rate_limiter_middleware(request: Request, call_next):
    ip = request.client.host
    now = time.time()

    with lock:
        if ip in BLOCKED_IPS and now < BLOCKED_IPS[ip]:
            return JSONResponse(
                status_code=429,
                content={"error": "IP blocked. Try again later."}
            )

        if ip not in REQUEST_LOG:
            REQUEST_LOG[ip] = deque()

        timestamps = REQUEST_LOG[ip]

        while timestamps and timestamps[0] <= now - WINDOW:
            timestamps.popleft()

        if len(timestamps) >= LIMIT:
            BLOCKED_IPS[ip] = now + BLOCK_DURATION
            REQUEST_LOG[ip].clear()
            return JSONResponse(
                status_code=429,
                content={"error": "Too many requests. IP blocked."}
            )

        timestamps.append(now)

    response = await call_next(request)
    return response


@app.get("/")
async def read_root():
    return {"message": "Welcome to the MMM auth API"}
