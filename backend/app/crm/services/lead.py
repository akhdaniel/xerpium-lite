from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.crm.models.lead import Lead
from backend.app.crm.schemas.lead import LeadCreate, LeadUpdate

def get_lead(db: Session, lead_id: int) -> Optional[Lead]:
    return db.query(Lead).filter(Lead.id == lead_id).first()

def get_leads(db: Session, skip: int = 0, limit: int = 100) -> List[Lead]:
    return db.query(Lead).offset(skip).limit(limit).all()

def create_lead(db: Session, lead: LeadCreate) -> Lead:
    db_lead = Lead(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def update_lead(db: Session, lead_id: int, lead: LeadUpdate) -> Optional[Lead]:
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if db_lead:
        for key, value in lead.dict(exclude_unset=True).items():
            setattr(db_lead, key, value)
        db.commit()
        db.refresh(db_lead)
    return db_lead

def delete_lead(db: Session, lead_id: int) -> Optional[Lead]:
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if db_lead:
        db.delete(db_lead)
        db.commit()
    return db_lead
