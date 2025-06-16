from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class ModelPlane(SQLModel, table=True):
    id_model: Optional[int] = Field(default=None, primary_key=True)
    name: str
    manufacturer: str
    capacity: int

    seats: List["Seat"] = Relationship(back_populates="model")
    planes: List["Plane"] = Relationship(back_populates="model")