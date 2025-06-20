from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from sqlalchemy import Column, Text
import json

class Airport(SQLModel, table=True):
    id_airport: Optional[int] = Field(default=None, primary_key=True)
    name: str
    iata: str
    city: str
    country: str
    image_urls: Optional[str] = Field(default="[]", sa_column=Column(Text))


    departures: List["Flight"] = Relationship(back_populates="departure_airport", sa_relationship_kwargs={"foreign_keys": "[Flight.departure_airport_id]"})
    arrivals: List["Flight"] = Relationship(back_populates="arrival_airport", sa_relationship_kwargs={"foreign_keys": "[Flight.arrival_airport_id]"})

    def get_image_urls(self) -> List[str]:
        return json.loads(self.image_urls or "[]")

    def set_image_urls(self, urls: List[str]):
        self.image_urls = json.dumps(urls)