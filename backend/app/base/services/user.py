from sqlalchemy.orm import Session
from backend.app.base.models.user import User
from backend.app.base.schemas.user import UserCreate, UserUpdate, UserInDB
from backend.app.base.models.user_group import UserGroup
from backend.app.base.security import get_password_hash # Import the hashing utility

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password) # Use the hashing utility
    db_user = User(email=user.email, hashed_password=hashed_password, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    user_data = user.dict(exclude_unset=True)
    if "password" in user_data:
        user_data["hashed_password"] = get_password_hash(user_data["password"])
        del user_data["password"]
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

def add_group_to_user(db: Session, user_id: int, group_id: int):
    db_user_group = UserGroup(user_id=user_id, group_id=group_id)
    db.add(db_user_group)
    db.commit()
    db.refresh(db_user_group)
    return db_user_group

def remove_group_from_user(db: Session, user_id: int, group_id: int):
    db_user_group = db.query(UserGroup).filter(
        UserGroup.user_id == user_id,
        UserGroup.group_id == group_id
    ).first()
    if not db_user_group:
        return None
    db.delete(db_user_group)
    db.commit()
    return db_user_group
