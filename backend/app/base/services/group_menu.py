from sqlalchemy.orm import Session
from backend.app.base.models.group_menu import GroupMenu
from backend.app.base.schemas.group_menu import GroupMenuCreate

def create_group_menu(db: Session, group_menu: GroupMenuCreate):
    db_group_menu = GroupMenu(**group_menu.dict())
    db.add(db_group_menu)
    db.commit()
    db.refresh(db_group_menu)
    return db_group_menu

def get_group_menu(db: Session, group_id: int, menu_id: int):
    return db.query(GroupMenu).filter(
        GroupMenu.group_id == group_id,
        GroupMenu.menu_id == menu_id
    ).first()

def get_group_menus_by_group(db: Session, group_id: int):
    return db.query(GroupMenu).filter(GroupMenu.group_id == group_id).all()

def delete_group_menu(db: Session, group_id: int, menu_id: int):
    db_group_menu = get_group_menu(db, group_id, menu_id)
    if not db_group_menu:
        return None
    db.delete(db_group_menu)
    db.commit()
    return db_group_menu
