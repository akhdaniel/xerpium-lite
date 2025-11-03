from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.app.base.services import menu as menu_service
from backend.app.base.schemas.menu import MenuCreate, MenuUpdate, Menu

def register_menu_item(db: Session, module: str, menu_item_data: Dict[str, Any]):
    # Check if menu item with this ID already exists
    existing_menu = menu_service.get_menu(db, menu_path=menu_item_data["path"])
    if existing_menu:
        # Update existing menu item
        menu_update = MenuUpdate(**menu_item_data)
        return menu_service.update_menu(db, menu_id=menu_item_data["id"], menu=menu_update)
    else:
        # Create new menu item
        menu_create = MenuCreate(**menu_item_data)
        return menu_service.create_menu(db=db, menu=menu_create)

def get_menu_items_by_module(db: Session, module: str) -> List[Dict[str, Any]]:
    menus = menu_service.get_menus(db)
    module_menus = [Menu.from_orm(menu).dict() for menu in menus if menu.module == module]
    return module_menus

def get_all_menu_items(db: Session) -> List[Dict[str, Any]]:
    menus = menu_service.get_menus(db)
    return [Menu.from_orm(menu).dict() for menu in menus]

def build_menu_hierarchy(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    import pprint 
    pprint.pprint(items)
    # Create a dictionary for quick lookup by id
    item_map = {item['id']: item for item in items}

    # Initialize children list for each item
    for item in items:
        item['children'] = []

    # Build the hierarchy
    root_items = []
    for item in items:
        if item.get('parent_id') is None:
            root_items.append(item)
        else:
            parent = item_map.get(item['parent_id'])
            if parent:
                parent['children'].append(item)
    
    # Sort root items and their children by 'order' if available
    def sort_by_order(item):
        return item.get('order', 0)

    root_items.sort(key=sort_by_order)
    for item in root_items:
        item['children'].sort(key=sort_by_order)

    return root_items
