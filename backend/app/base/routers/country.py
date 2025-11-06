from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.base.schemas.country import Country, CountryCreate, CountryUpdate
from backend.app.base.services import country as country_service
from backend.app.database import get_db

router = APIRouter()

@router.post("/", response_model=Country)
def create_country(country: CountryCreate, db: Session = Depends(get_db)):
    db_country = country_service.get_country_by_name(db, name=country.name)
    if db_country:
        raise HTTPException(status_code=400, detail="Country with this name already exists")
    return country_service.create_country(db=db, country=country)

@router.get("/", response_model=List[Country])
def read_countries(q: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    countries = country_service.get_countries(db, q=q, skip=skip, limit=limit)
    return countries

@router.get("/autocomplete", response_model=List[Country])
def autocomplete_countries(q: Optional[str] = None, db: Session = Depends(get_db)):
    countries = country_service.get_countries(db, q=q, limit=10) # Limit to 10 suggestions
    return countries

@router.get("/{country_id}", response_model=Country)
def read_country(country_id: int, db: Session = Depends(get_db)):
    db_country = country_service.get_country(db, country_id=country_id)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country

@router.put("/{country_id}", response_model=Country)
def update_country(country_id: int, country: CountryUpdate, db: Session = Depends(get_db)):
    db_country = country_service.update_country(db, country_id=country_id, country=country)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country

@router.delete("/{country_id}", response_model=Country)
def delete_country(country_id: int, db: Session = Depends(get_db)):
    db_country = country_service.delete_country(db, country_id=country_id)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country
