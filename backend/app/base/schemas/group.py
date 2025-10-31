from pydantic import BaseModel
from typing import Optional, List

from backend.app.base.schemas.group_access_right import GroupAccessRight
from backend.app.base.schemas.group_menu import GroupMenu
from backend.app.base.schemas.user_group import UserGroup

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None

class GroupCreate(GroupBase):
    pass

class GroupUpdate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    access_rights: List[GroupAccessRight] = []
    menus: List[GroupMenu] = []
    users: List[UserGroup] = []

    class Config:
        orm_mode = True
