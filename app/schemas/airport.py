from pydantic import Field
from typing import Annotated
from typing import Optional, List
from pydantic import BaseModel

IATACode = Annotated[str, Field(min_length=3, max_length=3, pattern="^[A-Z]{3}$")]


class AirportBase(BaseModel):
    name: str
    iata: IATACode
    city: str
    country: str
    image_urls: Optional[List[str]] = []


class AirportCreate(BaseModel):
    name: str
    iata: str
    city: str
    country: str
    image_urls: Optional[List[str]] = []

class AirportUpdate(BaseModel):
    name: Optional[str] = None
    iata: Optional[IATACode] = None
    city: Optional[str] = None
    country: Optional[str] = None
    image_urls: Optional[List[str]] = []


class AirportRead(AirportBase):
    id_airport: int
    name: str
    iata: IATACode
    city: str
    country: str
    image_urls: Optional[List[str]] = []

    class Config:
        from_attributes = True
