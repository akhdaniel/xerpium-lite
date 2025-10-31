from typing import List, Dict, Any

dashboard_items: Dict[str, List[Dict[str, Any]]] = {}

def register_dashboard_item(module: str, dashboard_item: Dict[str, Any]):
    if module not in dashboard_items:
        dashboard_items[module] = []
    dashboard_items[module].append(dashboard_item)

def get_dashboard_items_by_module(module: str) -> List[Dict[str, Any]]:
    return dashboard_items.get(module, [])

def get_all_dashboard_items() -> Dict[str, List[Dict[str, Any]]]:
    return dashboard_items
