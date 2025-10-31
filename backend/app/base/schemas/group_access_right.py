from pydantic import BaseModel
from typing import Optional

class GroupAccessRightBase(BaseModel):
    group_id: int
    access_right_id: int
    can_read: bool = False
    can_create: bool = False
    can_update: bool = False
    can_delete: bool = False

class GroupAccessRightCreate(GroupAccessRightBase):
    pass

class GroupAccessRight(GroupAccessRightBase):
    class Config:
        orm_mode = True
