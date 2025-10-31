from sqlalchemy import Column, Integer, String, DateTime, func
from backend.app.base.models.base import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, nullable=True)
    company = Column(String, nullable=True)
    status = Column(String, default="New") # e.g., New, Contacted, Qualified, Unqualified
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Lead(id={self.id}, name='{self.first_name} {self.last_name}', email='{self.email}')>"