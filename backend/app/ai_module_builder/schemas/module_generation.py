from pydantic import BaseModel

class ModuleSpecification(BaseModel):
    name: str
    specification: str
