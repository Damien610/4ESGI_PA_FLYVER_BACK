from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class FlightBase(BaseModel):
    plane_id: int
    departure_airport_id: int
    arrival_airport_id: int
    departure_time: datetime
    arrival_time: datetime


class FlightCreate(FlightBase):
    pass


class FlightUpdate(BaseModel):
    plane_id: Optional[int] = None
    departure_airport_id: Optional[int] = None
    arrival_airport_id: Optional[int] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None


class FlightRead(FlightBase):
    id_flight: int

    class Config:
        from_attributes = True
