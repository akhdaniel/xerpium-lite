from sqlalchemy import Column, Integer, String
from backend.app.base.models.base import Base

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    def __repr__(self):
        return f"<Country(id={self.id}, name='{self.name}')>"