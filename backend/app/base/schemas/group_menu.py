from pydantic import BaseModel

class GroupMenuBase(BaseModel):
    group_id: int
    menu_id: int

class GroupMenuCreate(GroupMenuBase):
    pass

class GroupMenu(GroupMenuBase):
    class Config:
        orm_mode = True
