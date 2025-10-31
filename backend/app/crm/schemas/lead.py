from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = "New"

class LeadCreate(LeadBase):
    pass

class LeadUpdate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
