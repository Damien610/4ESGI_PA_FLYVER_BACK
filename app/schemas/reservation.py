from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ReservationBase(BaseModel):
    flight_id: int
    passenger_id: int


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(BaseModel):
    flight_id: Optional[int] = None
    passenger_id: Optional[int] = None


class ReservationRead(ReservationBase):
    id_reservation: int
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2, remplace orm_mode = True
