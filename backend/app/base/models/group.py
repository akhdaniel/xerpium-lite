from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    access_rights = relationship("GroupAccessRight", back_populates="group")
    menus = relationship("GroupMenu", back_populates="group")
    users = relationship("UserGroup", back_populates="group")

    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}')>"
