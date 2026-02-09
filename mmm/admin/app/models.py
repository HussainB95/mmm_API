from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SpecialInterestBase(BaseModel):
    slug: str
    title: str
    content: Optional[str] = None
    thumbnail: Optional[str] = None
    status: Optional[str] = "draft"
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None

class SpecialInterestCreate(SpecialInterestBase):
    pass

class SpecialInterestOut(SpecialInterestBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 
