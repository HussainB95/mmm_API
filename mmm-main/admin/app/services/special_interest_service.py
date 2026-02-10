from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SpecialInterest(BaseModel):   # <-- rename
    id: int
    slug: str
    title: str
    content: Optional[str] = None
    thumbnail: Optional[str] = None
    status: Optional[str] = "draft"
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    created_at: datetime
    updated_at: datetime