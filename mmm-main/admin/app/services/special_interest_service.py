from pydantic import BaseModel #this file is for Pydantic
from datetime import datetime
from typing import Optional

class SpecialInterest(BaseModel):   # <-- rename
    id: int
    title: str