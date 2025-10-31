from sqlalchemy.orm import Session
from backend.app.database import SessionLocal, engine, Base
from backend.app.base.models.user import User
from backend.app.base.security import verify_password

def check_admin_user(db: Session):
    admin_email = "admin@example.com"
    admin_password = "adminpass"

    user = db.query(User).filter(User.email == admin_email).first()

    if user:
        print(f"User found: {user.email}")
        print(f"Hashed password in DB: {user.hashed_password}")
        if verify_password(admin_password, user.hashed_password):
            print("Password verification successful!")
        else:
            print("Password verification FAILED!")
    else:
        print(f"User with email {admin_email} NOT found.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        check_admin_user(db)
    finally:
        db.close()
