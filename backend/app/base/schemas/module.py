from pydantic import BaseModel
from typing import Optional

class ModuleBase(BaseModel):
    name: str
    is_active: bool = True

class ModuleCreate(ModuleBase):
    pass

class ModuleUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None

class Module(ModuleBase):
    id: int

    class Config:
        orm_mode = True
