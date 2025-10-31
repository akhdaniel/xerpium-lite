from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import as_declarative
from sqlalchemy.ext.declarative import declared_attr

@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
