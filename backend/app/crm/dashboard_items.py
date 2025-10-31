from sqlalchemy.orm import Session
from backend.app.base.dashboard_registry import register_dashboard_item
from backend.app.crm.models.customer import Customer

def get_customer_count(db: Session):
    return db.query(Customer).count()

def get_dummy_table_data(db):
    return {
        "headers": ["Name", "Value"],
        "rows": [
            ["Dummy 1", 100],
            ["Dummy 2", 200]
        ]
    }

def register_crm_dashboard_items():
    register_dashboard_item("crm", {
        "id": "customer_count",
        "title": "Number of Partners",
        "type": "kpi_card",
        "service": get_customer_count,
    })
    register_dashboard_item("crm", {
        "id": "crm_dummy_item",
        "title": "CRM Dummy Table",
        "type": "table",
        "service": get_dummy_table_data,
    })
