from sqlalchemy.orm import Session, joinedload
from backend.app.crm.models.customer import Customer
from backend.app.crm.models.address import Address
from backend.app.crm.schemas.customer import CustomerCreate, CustomerUpdate

def get_customer(db: Session, customer_id: int):
    return db.query(Customer).options(joinedload(Customer.addresses)).filter(Customer.id == customer_id).first()

def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).options(joinedload(Customer.addresses)).filter(Customer.email == email).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).options(joinedload(Customer.addresses)).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: CustomerCreate):
    customer_data = customer.dict(exclude={'addresses'})
    db_customer = Customer(**customer_data)
    
    for address_data in customer.addresses:
        address_dict = address_data.dict()
        address_dict.pop('country', None)
        db_address = Address(**address_dict, customer=db_customer)
        db.add(db_address)
        
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return get_customer(db, db_customer.id)

def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
        
    customer_data = customer.dict(exclude_unset=True, exclude={'addresses'})
    for key, value in customer_data.items():
        setattr(db_customer, key, value)

    if customer.addresses is not None:
        # Simple approach: delete existing and create new ones
        for address in db_customer.addresses:
            db.delete(address)
        
        for address_data in customer.addresses:
            address_dict = address_data.dict()
            address_dict.pop('country', None)
            db_address = Address(**address_dict, customer_id=customer_id)
            db.add(db_address)

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
