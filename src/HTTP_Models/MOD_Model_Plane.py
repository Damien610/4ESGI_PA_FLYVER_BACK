from pydantic import BaseModel
from typing import Optional

class ModeleCreateModels(BaseModel):
    name: str
    manufacturer: str
    capacity: int

class ModeleUpdateModel(BaseModel):
    name: Optional[str] = None
    manufacturer: Optional[str] = None
    capacity: Optional[int] = None
