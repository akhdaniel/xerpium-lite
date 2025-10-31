from sqlalchemy.orm import Session, joinedload
from backend.app.crm.models.customer import Customer
from backend.app.crm.schemas.customer import CustomerCreate, CustomerUpdate
from backend.app.crm.models.country import Country

def get_customer(db: Session, customer_id: int):
    return db.query(Customer).options(joinedload(Customer.country)).filter(Customer.id == customer_id).first()

def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).options(joinedload(Customer.country)).filter(Customer.email == email).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).options(joinedload(Customer.country)).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: CustomerCreate):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return get_customer(db, db_customer.id)

def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
    customer_data = customer.dict(exclude_unset=True)
    for key, value in customer_data.items():
        setattr(db_customer, key, value)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return get_customer(db, customer_id)

def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
    db.delete(db_customer)
    db.commit()
    return db_customer
