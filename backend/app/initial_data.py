from sqlalchemy.orm import Session
from backend.app.database import engine, Base
from backend.app.base.models.user import User
from backend.app.base.models.group import Group
from backend.app.base.models.access_right import AccessRight
from backend.app.base.models.user_group import UserGroup
from backend.app.base.models.group_access_right import GroupAccessRight
from backend.app.crm.models.country import Country
from backend.app.crm.models.customer import Customer
from backend.app.base.security import get_password_hash

def create_initial_data(db: Session):
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create Admin Group if it doesn't exist
    admin_group = db.query(Group).filter(Group.name == "Admin").first()
    if not admin_group:
        admin_group = Group(name="Admin", description="Administrator group with full access")
        db.add(admin_group)
        db.flush()  # Use flush to get the id before commit
        print("Admin group created.")
    else:
        print("Admin group already exists.")

    # Create Admin User if it doesn't exist
    admin_user = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("adminpass")
        )
        db.add(admin_user)
        db.flush()  # Use flush to get the id before commit
        print("Admin user created.")
    else:
        print("Admin user already exists.")

    # Associate Admin User with Admin Group if not already associated
    user_group = db.query(UserGroup).filter(
        UserGroup.user_id == admin_user.id,
        UserGroup.group_id == admin_group.id
    ).first()
    if not user_group:
        user_group = UserGroup(user_id=admin_user.id, group_id=admin_group.id)
        db.add(user_group)
        print("Admin user associated with Admin group.")
    else:
        print("Admin user already associated with Admin group.")

    # Define all models for access rights
    model_names = [
        "User", "Group", "AccessRight", "Menu", "Customer", "Lead", "Opportunity", "Country",
        "UserGroup", "GroupAccessRight", "GroupMenu", "Dashboard", "UI_Schema"
    ]

    # Create initial Country data if it doesn't exist
    countries_data = [
        {"name": "USA"},
        {"name": "Canada"},
        {"name": "Mexico"},
        {"name": "Germany"},
        {"name": "France"},
        {"name": "Spain"},
        {"name": "Italy"},
        {"name": "United Kingdom"},
        {"name": "Australia"},
        {"name": "Japan"},
    ]

    for country_data in countries_data:
        country = db.query(Country).filter(Country.name == country_data["name"]).first()
        if not country:
            country = Country(**country_data)
            db.add(country)
            db.flush()
            print(f"Country {country.name} created.")
        else:
            print(f"Country {country.name} already exists.")

    # Create sample Customer data if it doesn't exist
    customer1 = db.query(Customer).filter(Customer.email == "john.doe@example.com").first()
    if not customer1:
        usa_country = db.query(Country).filter(Country.name == "USA").first()
        customer1 = Customer(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="123-456-7890",
            address="123 Main St, Anytown, USA",
            country_id=usa_country.id if usa_country else None
        )
        db.add(customer1)
        print("Sample customer John Doe created.")
    else:
        print("Sample customer John Doe already exists.")

    customer2 = db.query(Customer).filter(Customer.email == "jane.smith@example.com").first()
    if not customer2:
        canada_country = db.query(Country).filter(Country.name == "Canada").first()
        customer2 = Customer(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            phone_number="098-765-4321",
            address="456 Oak Ave, Otherville, Canada",
            country_id=canada_country.id if canada_country else None
        )
        db.add(customer2)
        print("Sample customer Jane Smith created.")
    else:
        print("Sample customer Jane Smith already exists.")

    for model_name in model_names:
        access_right = db.query(AccessRight).filter(AccessRight.name == model_name).first()
        if not access_right:
            access_right = AccessRight(name=model_name, description=f"Access to {model_name} model")
            db.add(access_right)
            db.flush()
            print(f"AccessRight for {model_name} created.")
        else:
            print(f"AccessRight for {model_name} already exists.")

        # Assign all permissions to Admin Group
        group_access_right = db.query(GroupAccessRight).filter(
            GroupAccessRight.group_id == admin_group.id,
            GroupAccessRight.access_right_id == access_right.id
        ).first()
        if not group_access_right:
            group_access_right = GroupAccessRight(
                group_id=admin_group.id,
                access_right_id=access_right.id,
                can_read=True,
                can_create=True,
                can_update=True,
                can_delete=True
            )
            db.add(group_access_right)
            print(f"All permissions for {model_name} assigned to Admin group.")
        else:
            print(f"All permissions for {model_name} already assigned to Admin group.")

    db.commit()
