from pydantic import BaseModel
from typing import List

class FieldInfo(BaseModel):
    name: str
    field_type: str

class ModelInfo(BaseModel):
    name: str
    fields: List[FieldInfo]
