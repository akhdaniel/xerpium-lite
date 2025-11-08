from typing import List, Dict, Any

dashboard_items: List[Dict[str, Any]] = []

def register_dashboard_item(item: Dict[str, Any]):
    dashboard_items.append(item)

def get_dashboard_items() -> List[Dict[str, Any]]:
    return dashboard_items

def register_inventory_dashboard_items():
    register_dashboard_item({
        "id": "inventory_products_count",
        "title": "Total Products",
        "type": "metric",
        "data_url": "/inventory/dashboard/products_count",
        "icon": "bi-box-seam",
        "color": "primary"
    })
    register_dashboard_item({
        "id": "inventory_warehouses_count",
        "title": "Total Warehouses",
        "type": "metric",
        "data_url": "/inventory/dashboard/warehouses_count",
        "icon": "bi-building",
        "color": "info"
    })
    register_dashboard_item({
        "id": "inventory_locations_count",
        "title": "Total Locations",
        "type": "metric",
        "data_url": "/inventory/dashboard/locations_count",
        "icon": "bi-geo-alt",
        "color": "success"
    })
