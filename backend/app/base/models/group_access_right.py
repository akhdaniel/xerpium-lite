from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class GroupAccessRight(Base):
    __tablename__ = "group_access_rights"

    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    access_right_id = Column(Integer, ForeignKey("access_rights.id"), primary_key=True)
    can_read = Column(Boolean, default=False)
    can_create = Column(Boolean, default=False)
    can_update = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)

    group = relationship("Group", back_populates="access_rights")
    access_right = relationship("AccessRight")

    def __repr__(self):
        return f"<GroupAccessRight(group_id={self.group_id}, access_right_id={self.access_right_id})>"
