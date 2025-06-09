from pydantic import BaseModel
from typing import Optional

class AirportCreateModel(BaseModel):
    name: str
    iata: str
    city: str
    country: str

class AirportUpdateModel(BaseModel):
    name: Optional[str] = None
    iata: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None