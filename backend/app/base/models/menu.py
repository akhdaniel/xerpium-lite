from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    path = Column(String, unique=True, nullable=False)
    icon = Column(String, nullable=True)
    parent_id = Column(Integer, ForeignKey('menus.id'), nullable=True)
    order = Column(Integer, default=0)
    module = Column(String, nullable=False)

    parent = relationship("Menu", remote_side='Menu.id', backref="children")

    def __repr__(self):
        return f"<Menu(id={self.id}, name='{self.name}', path='{self.path}')>"
