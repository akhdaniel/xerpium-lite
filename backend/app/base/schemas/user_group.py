from pydantic import BaseModel

class UserGroupBase(BaseModel):
    user_id: int
    group_id: int

class UserGroupCreate(UserGroupBase):
    pass

class UserGroup(UserGroupBase):
    class Config:
        orm_mode = True
