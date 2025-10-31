from sqlalchemy.orm import Session
from backend.app.base.models.user_group import UserGroup
from backend.app.base.schemas.user_group import UserGroupCreate

def create_user_group(db: Session, user_group: UserGroupCreate):
    db_user_group = UserGroup(**user_group.dict())
    db.add(db_user_group)
    db.commit()
    db.refresh(db_user_group)
    return db_user_group

def get_user_group(db: Session, user_id: int, group_id: int):
    return db.query(UserGroup).filter(
        UserGroup.user_id == user_id,
        UserGroup.group_id == group_id
    ).first()

def get_user_groups_by_user(db: Session, user_id: int):
    return db.query(UserGroup).filter(UserGroup.user_id == user_id).all()

def delete_user_group(db: Session, user_id: int, group_id: int):
    db_user_group = get_user_group(db, user_id, group_id)
    if not db_user_group:
        return None
    db.delete(db_user_group)
    db.commit()
    return db_user_group
