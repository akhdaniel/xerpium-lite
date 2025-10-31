from sqlalchemy.orm import Session
from backend.app.base.models.group_access_right import GroupAccessRight
from backend.app.base.schemas.group_access_right import GroupAccessRightCreate

def create_group_access_right(db: Session, group_access_right: GroupAccessRightCreate):
    db_group_access_right = GroupAccessRight(**group_access_right.dict())
    db.add(db_group_access_right)
    db.commit()
    db.refresh(db_group_access_right)
    return db_group_access_right

def get_group_access_right(db: Session, group_id: int, access_right_id: int):
    return db.query(GroupAccessRight).filter(
        GroupAccessRight.group_id == group_id,
        GroupAccessRight.access_right_id == access_right_id
    ).first()

def get_group_access_rights_by_group(db: Session, group_id: int):
    return db.query(GroupAccessRight).filter(GroupAccessRight.group_id == group_id).all()

def delete_group_access_right(db: Session, group_id: int, access_right_id: int):
    db_group_access_right = get_group_access_right(db, group_id, access_right_id)
    if not db_group_access_right:
        return None
    db.delete(db_group_access_right)
    db.commit()
    return db_group_access_right
