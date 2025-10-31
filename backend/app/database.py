from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.base.models.base import Base

SQLALCHEMY_DATABASE_URL = "sqlite:////Users/daniel/data/xerpium1/sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    print("Attempting to create database tables...")
    Base.metadata.create_all(engine)
    print("Database tables creation attempt finished.")