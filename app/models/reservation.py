from dataclasses import Field
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

from app.models.flight import Flight
from app.models.passenger import Passenger
from app.models.seat import Seat


class Reservation(SQLModel, table=True):
    id_reservation: Optional[int] = Field(default=None, primary_key=True)
    flight_id: int = Field(foreign_key="flight.id_flight")
    passenger_id: int = Field(foreign_key="passengers.id_passenger")
    seat_id: int = Field(foreign_key="seat.id_seat")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    flight: Optional[Flight] = Relationship(back_populates="reservations")
    passenger: Optional[Passenger] = Relationship(back_populates="reservations")
    seat: Optional[Seat] = Relationship(back_populates="reservations")