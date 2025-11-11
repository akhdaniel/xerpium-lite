from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class GenerationLogBase(BaseModel):
    module_name: str
    specification: str
    detailed_specification: Optional[str] = None
    generated_files: Optional[List[str]] = None

class GenerationLogCreate(GenerationLogBase):
    pass

class GenerationLogUpdate(GenerationLogBase):
    pass

class GenerationLog(GenerationLogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
