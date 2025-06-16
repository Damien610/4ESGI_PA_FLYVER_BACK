from pydantic import BaseModel, Field
from typing import Annotated, Optional
from datetime import datetime


# Contraintes IATA : 3 lettres majuscules
IATACode = Annotated[str, Field(min_length=3, max_length=3, pattern="^[A-Z]{3}$")]


class AirportBase(BaseModel):
    name: str
    iata: IATACode
    city: str
    country: str


class AirportCreate(AirportBase):
    pass


class AirportUpdate(BaseModel):
    name: Optional[str] = None
    iata: Optional[IATACode] = None
    city: Optional[str] = None
    country: Optional[str] = None


class AirportRead(AirportBase):
    id_airport: int
    name: str
    iata: IATACode
    city: str
    country: str
    class Config:
        from_attributes = True
