from sqlalchemy.orm import Session
from backend.app.base.dashboard_registry import register_dashboard_item
from backend.app.base.models.user import User
from backend.app.base.models.group import Group
from backend.app.base.models.user_group import UserGroup
from sqlalchemy import func

def get_user_count(db: Session):
    return db.query(User).count()

def get_group_count(db: Session):
    return db.query(Group).count()

def get_users_per_group(db: Session):
    results = db.query(Group.name, func.count(UserGroup.user_id)).select_from(Group).outerjoin(UserGroup, Group.id == UserGroup.group_id).group_by(Group.name).all()
    return {
        "labels": [result[0] for result in results],
        "datasets": [{
            "label": "Users per Group",
            "data": [result[1] for result in results],
            "backgroundColor": [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            "borderColor": [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            "borderWidth": 1
        }]
    }

def register_base_dashboard_items():
    register_dashboard_item("base", {
        "id": "user_count",
        "title": "Number of Users",
        "type": "number_card",
        "service": get_user_count,
    })
    register_dashboard_item("base", {
        "id": "group_count",
        "title": "Number of Companies",
        "type": "number_card",
        "service": get_group_count,
    })
    register_dashboard_item("base", {
        "id": "users_per_group",
        "title": "Users per Group",
        "type": "chart",
        "chart_type": "bar",
        "service": get_users_per_group,
    })
