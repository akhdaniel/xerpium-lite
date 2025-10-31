from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.crm.models.opportunity import Opportunity
from backend.app.crm.schemas.opportunity import OpportunityCreate, OpportunityUpdate

def get_opportunity(db: Session, opportunity_id: int) -> Optional[Opportunity]:
    return db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()

def get_opportunities(db: Session, skip: int = 0, limit: int = 100) -> List[Opportunity]:
    return db.query(Opportunity).offset(skip).limit(limit).all()

def create_opportunity(db: Session, opportunity: OpportunityCreate) -> Opportunity:
    db_opportunity = Opportunity(**opportunity.dict())
    db.add(db_opportunity)
    db.commit()
    db.refresh(db_opportunity)
    return db_opportunity

def update_opportunity(db: Session, opportunity_id: int, opportunity: OpportunityUpdate) -> Optional[Opportunity]:
    db_opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if db_opportunity:
        for key, value in opportunity.dict(exclude_unset=True).items():
            setattr(db_opportunity, key, value)
        db.commit()
        db.refresh(db_opportunity)
    return db_opportunity

def delete_opportunity(db: Session, opportunity_id: int) -> Optional[Opportunity]:
    db_opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if db_opportunity:
        db.delete(db_opportunity)
        db.commit()
    return db_opportunity
