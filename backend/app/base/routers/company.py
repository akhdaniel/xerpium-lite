from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.base.schemas.company import Company, CompanyCreate, CompanyUpdate
from backend.app.base.services import company as company_service
from backend.app.base.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=Company)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = company_service.get_company_by_name(db, name=company.name)
    if db_company:
        raise HTTPException(status_code=400, detail="Company with this name already exists")
    return company_service.create_company(db=db, company=company)

@router.get("/", response_model=List[Company])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companies = company_service.get_companies(db, skip=skip, limit=limit)
    return companies

@router.get("/{company_id}", response_model=Company)
def read_company(company_id: int, db: Session = Depends(get_db)):
    db_company = company_service.get_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@router.put("/{company_id}", response_model=Company)
def update_company(company_id: int, company: CompanyUpdate, db: Session = Depends(get_db)):
    db_company = company_service.update_company(db, company_id=company_id, company=company)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@router.delete("/{company_id}", response_model=Company)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    db_company = company_service.delete_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company
