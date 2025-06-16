from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Airport(SQLModel, table=True):
    id_airport: Optional[int] = Field(default=None, primary_key=True)
    name: str
    iata: str
    city: str
    country: str

    departures: List["Flight"] = Relationship(back_populates="departure_airport", sa_relationship_kwargs={"foreign_keys": "[Flight.departure_airport_id]"})
    arrivals: List["Flight"] = Relationship(back_populates="arrival_airport", sa_relationship_kwargs={"foreign_keys": "[Flight.arrival_airport_id]"})