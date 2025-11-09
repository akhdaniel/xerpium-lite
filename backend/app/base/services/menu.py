from sqlalchemy.orm import Session
from backend.app.base.models.menu import Menu
from backend.app.base.schemas.menu import MenuCreate, MenuUpdate

def get_menu(db: Session, menu_id: int):
    return db.query(Menu).filter(Menu.id == menu_id).first()

def get_menus(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Menu).offset(skip).limit(limit).all()

def create_menu(db: Session, menu: MenuCreate):
    import pprint
    pprint.pprint(menu)
    db_menu = Menu(**menu.dict())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

def update_menu(db: Session, menu_id: int, menu: MenuUpdate):
    db_menu = get_menu(db, menu_id)
    if not db_menu:
        return None
    menu_data = menu.dict(exclude_unset=True)
    for key, value in menu_data.items():
        setattr(db_menu, key, value)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

def delete_menu(db: Session, menu_id: int):
    db_menu = get_menu(db, menu_id)
    if not db_menu:
        return None
    db.delete(db_menu)
    db.commit()
    return db_menu
