from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.base.models.country import Country
from backend.app.base.schemas.country import CountryCreate, CountryUpdate

def get_country(db: Session, country_id: int) -> Optional[Country]:
    return db.query(Country).filter(Country.id == country_id).first()

def get_country_by_name(db: Session, name: str) -> Optional[Country]:
    return db.query(Country).filter(Country.name == name).first()

def get_countries(db: Session, q: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Country]:
    query = db.query(Country)
    if q:
        query = query.filter(Country.name.ilike(f"%{q}%"))
    return query.offset(skip).limit(limit).all()

def create_country(db: Session, country: CountryCreate) -> Country:
    db_country = Country(**country.dict())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

def update_country(db: Session, country_id: int, country: CountryUpdate) -> Optional[Country]:
    db_country = db.query(Country).filter(Country.id == country_id).first()
    if db_country:
        for key, value in country.dict(exclude_unset=True).items():
            setattr(db_country, key, value)
        db.commit()
        db.refresh(db_country)
    return db_country

def delete_country(db: Session, country_id: int) -> Optional[Country]:
    db_country = db.query(Country).filter(Country.id == country_id).first()
    if db_country:
        db.delete(db_country)
        db.commit()
    return db_country
