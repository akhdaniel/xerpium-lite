from pydantic import BaseModel
from typing import Optional

class AccessRightBase(BaseModel):
    name: str
    description: Optional[str] = None

class AccessRightCreate(AccessRightBase):
    pass

class AccessRightUpdate(AccessRightBase):
    pass

class AccessRight(AccessRightBase):
    id: int

    class Config:
        orm_mode = True
