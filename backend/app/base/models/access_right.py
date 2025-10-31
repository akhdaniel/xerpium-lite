from sqlalchemy import Column, Integer, String
from .base import Base

class AccessRight(Base):
    __tablename__ = "access_rights"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    def __repr__(self):
        return f"<AccessRight(id={self.id}, name='{self.name}')>"
