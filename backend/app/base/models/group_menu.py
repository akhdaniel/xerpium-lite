from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class GroupMenu(Base):
    __tablename__ = "group_menus"

    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    menu_id = Column(Integer, ForeignKey("menus.id"), primary_key=True)

    group = relationship("Group", back_populates="menus")
    menu = relationship("Menu")

    def __repr__(self):
        return f"<GroupMenu(group_id={self.group_id}, menu_id={self.menu_id})>"
