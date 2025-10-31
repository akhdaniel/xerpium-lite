from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from backend.app.base.models.base import Base
from backend.app.crm.models.country import Country

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=True)
    birth_date = Column(DateTime, nullable=True)
    last_contacted = Column(DateTime, nullable=True)

    country = relationship("Country")

    def __repr__(self):
        return f"<Customer(id={self.id}, email='{self.email}')>"
