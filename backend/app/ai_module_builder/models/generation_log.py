from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.sql import func
from backend.app.database import Base

class GenerationLog(Base):
    __tablename__ = "ai_module_builder_generation_log"

    id = Column(Integer, primary_key=True, index=True)
    module_name = Column(String, index=True, nullable=False)
    specification = Column(Text, nullable=False)
    generated_files = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
