from pydantic import BaseModel
from typing import Optional, List

from backend.app.base.schemas.user_group import UserGroup

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    hashed_password: str

class User(UserBase):
    id: int
    groups: List[UserGroup] = []

    class Config:
        orm_mode = True
