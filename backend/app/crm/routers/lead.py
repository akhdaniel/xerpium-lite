from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.crm.schemas.lead import Lead, LeadCreate, LeadUpdate
from backend.app.crm.services import lead as lead_service
from backend.app.database import get_db

router = APIRouter()

@router.post("/", response_model=Lead)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    return lead_service.create_lead(db=db, lead=lead)

@router.get("/", response_model=List[Lead])
def read_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    leads = lead_service.get_leads(db, skip=skip, limit=limit)
    return leads

@router.get("/{lead_id}", response_model=Lead)
def read_lead(lead_id: int, db: Session = Depends(get_db)):
    db_lead = lead_service.get_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead

@router.put("/{lead_id}", response_model=Lead)
def update_lead(lead_id: int, lead: LeadUpdate, db: Session = Depends(get_db)):
    db_lead = lead_service.update_lead(db, lead_id=lead_id, lead=lead)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead

@router.delete("/{lead_id}", response_model=Lead)
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    db_lead = lead_service.delete_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead
