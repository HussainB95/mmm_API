import httpx
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

GOOGLE_CALENDAR_API = os.getenv("GOOGLE_CALENDAR_API")

async def create_calendar_event(access_token: str, summary: str, description: str, start_time: str, end_time: str):
    headers = {
        "Authorization" : f"Bearer {access_token}",
        "Content_Type" : "application/json"
    }

    event = {
        "summary" :summary,
        "description" :description,
        "start" : {
            "datetime" : start_time,
            "timezone" : "Asia/Kolkata"
        },
        "end" : {
            "datetime" : end_time,
            "timezone" : "Asia/Kolkata"
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            GOOGLE_CALENDAR_API,
            headers=headers,
            json=event
        )
    return response.json()