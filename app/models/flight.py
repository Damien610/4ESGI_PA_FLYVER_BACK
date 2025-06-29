from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

from app.models.airport import Airport
from app.models.plane import Plane


class Flight(SQLModel, table=True):
    id_flight: Optional[int] = Field(default=None, primary_key=True)
    plane_id: int = Field(foreign_key="plane.id_plane")
    departure_airport_id: int = Field(foreign_key="airport.id_airport")
    arrival_airport_id: int = Field(foreign_key="airport.id_airport")
    departure_time: datetime
    arrival_time: datetime

    plane: Optional[Plane] = Relationship(back_populates="flights")
    departure_airport: Optional[Airport] = Relationship(back_populates="departures", sa_relationship_kwargs={"foreign_keys": "[Flight.departure_airport_id]"})
    arrival_airport: Optional[Airport] = Relationship(back_populates="arrivals", sa_relationship_kwargs={"foreign_keys": "[Flight.arrival_airport_id]"})
    reservations: List["Reservation"] = Relationship(back_populates="flight")