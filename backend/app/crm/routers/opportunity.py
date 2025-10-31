from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.crm.schemas.opportunity import Opportunity, OpportunityCreate, OpportunityUpdate
from backend.app.crm.services import opportunity as opportunity_service
from backend.app.database import get_db

router = APIRouter()

@router.post("/", response_model=Opportunity)
def create_opportunity(opportunity: OpportunityCreate, db: Session = Depends(get_db)):
    return opportunity_service.create_opportunity(db=db, opportunity=opportunity)

@router.get("/", response_model=List[Opportunity])
def read_opportunities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    opportunities = opportunity_service.get_opportunities(db, skip=skip, limit=limit)
    return opportunities

@router.get("/{opportunity_id}", response_model=Opportunity)
def read_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    db_opportunity = opportunity_service.get_opportunity(db, opportunity_id=opportunity_id)
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return db_opportunity

@router.put("/{opportunity_id}", response_model=Opportunity)
def update_opportunity(opportunity_id: int, opportunity: OpportunityUpdate, db: Session = Depends(get_db)):
    db_opportunity = opportunity_service.update_opportunity(db, opportunity_id=opportunity_id, opportunity=opportunity)
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return db_opportunity

@router.delete("/{opportunity_id}", response_model=Opportunity)
def delete_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    db_opportunity = opportunity_service.delete_opportunity(db, opportunity_id=opportunity_id)
    if db_opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return db_opportunity
