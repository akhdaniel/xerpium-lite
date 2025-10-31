from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.base.models.base import Base
from sqlalchemy import DateTime, func

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    stage = Column(String, default="Prospecting") # e.g., Prospecting, Qualification, Proposal, Negotiation, Closed Won, Closed Lost
    close_date = Column(Date, nullable=True)
    lead_id = Column(Integer, ForeignKey('leads.id'), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    lead = relationship("Lead", backref="opportunities")

    def __repr__(self):
        return f"<Opportunity(id={self.id}, name='{self.name}', stage='{self.stage}')>"