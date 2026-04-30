from pydantic import BaseModel #this file is for Pydantic
from datetime import datetime
from typing import Optional

class SpecialInterest(BaseModel):
    id: int
    title: str