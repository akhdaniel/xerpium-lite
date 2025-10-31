from sqlalchemy.orm import Session
from backend.app.base.models.group import Group
from backend.app.base.schemas.group import GroupCreate, GroupUpdate
from backend.app.base.models.group_access_right import GroupAccessRight
from backend.app.base.models.group_menu import GroupMenu

def get_group(db: Session, group_id: int):
    return db.query(Group).filter(Group.id == group_id).first()

def get_group_by_name(db: Session, name: str):
    return db.query(Group).filter(Group.name == name).first()

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Group).offset(skip).limit(limit).all()

def create_group(db: Session, group: GroupCreate):
    db_group = Group(name=group.name, description=group.description)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def update_group(db: Session, group_id: int, group: GroupUpdate):
    db_group = get_group(db, group_id)
    if not db_group:
        return None
    group_data = group.dict(exclude_unset=True)
    for key, value in group_data.items():
        setattr(db_group, key, value)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def delete_group(db: Session, group_id: int):
    db_group = get_group(db, group_id)
    if not db_group:
        return None
    db.delete(db_group)
    db.commit()
    return db_group

def add_access_right_to_group(db: Session, group_id: int, access_right_id: int, can_read: bool, can_create: bool, can_update: bool, can_delete: bool):
    db_group_access_right = GroupAccessRight(
        group_id=group_id,
        access_right_id=access_right_id,
        can_read=can_read,
        can_create=can_create,
        can_update=can_update,
        can_delete=can_delete
    )
    db.add(db_group_access_right)
    db.commit()
    db.refresh(db_group_access_right)
    return db_group_access_right

def remove_access_right_from_group(db: Session, group_id: int, access_right_id: int):
    db_group_access_right = db.query(GroupAccessRight).filter(
        GroupAccessRight.group_id == group_id,
        GroupAccessRight.access_right_id == access_right_id
    ).first()
    if not db_group_access_right:
        return None
    db.delete(db_group_access_right)
    db.commit()
    return db_group_access_right

def add_menu_to_group(db: Session, group_id: int, menu_id: int):
    db_group_menu = GroupMenu(group_id=group_id, menu_id=menu_id)
    db.add(db_group_menu)
    db.commit()
    db.refresh(db_group_menu)
    return db_group_menu

def remove_menu_from_group(db: Session, group_id: int, menu_id: int):
    db_group_menu = db.query(GroupMenu).filter(
        GroupMenu.group_id == group_id,
        GroupMenu.menu_id == menu_id
    ).first()
    if not db_group_menu:
        return None
    db.delete(db_group_menu)
    db.commit()
    return db_group_menu
