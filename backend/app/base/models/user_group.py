from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class UserGroup(Base):
    __tablename__ = "user_groups"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)

    user = relationship("User", back_populates="groups")
    group = relationship("Group", back_populates="users")

    def __repr__(self):
        return f"<UserGroup(user_id={self.user_id}, group_id={self.group_id})>"
