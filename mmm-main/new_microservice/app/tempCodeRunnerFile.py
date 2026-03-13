from fastapi import FastAPI
from routers.practitioner_profile import router as practitioner_profile_router

app = FastAPI()

app.include_router(practitioner_profile_router)

import os
print("CURRENT DIR:", os.getcwd())
print("FILES:", os.listdir())