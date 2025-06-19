from dataclasses import Field
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

from app.models.flight import Flight
from app.models.passenger import Passenger



class Reservation(SQLModel, table=True):
    id_reservation: Optional[int] = Field(default=None, primary_key=True)
    flight_id: int = Field(foreign_key="flight.id_flight")
    passenger_id: int = Field(foreign_key="passengers.id_passenger")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    flight: Optional[Flight] = Relationship(back_populates="reservations")
    passenger: Optional[Passenger] = Relationship(back_populates="reservations")