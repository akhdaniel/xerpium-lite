from pydantic import BaseModel
from typing import Optional, List

class MenuBase(BaseModel):
    name: str
    path: str
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    order: int = 0
    module: str

class MenuCreate(MenuBase):
    pass

class MenuUpdate(MenuBase):
    pass

class Menu(MenuBase):
    id: int
    children: List['Menu'] = []

    class Config:
        from_attributes = True

Menu.update_forward_refs()
