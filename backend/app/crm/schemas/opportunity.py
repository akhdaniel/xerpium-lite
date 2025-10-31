from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

class OpportunityBase(BaseModel):
    name: str
    description: Optional[str] = None
    amount: float
    stage: Optional[str] = "Prospecting"
    close_date: Optional[date] = None
    lead_id: Optional[int] = None

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityUpdate(OpportunityBase):
    pass

class Opportunity(OpportunityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
