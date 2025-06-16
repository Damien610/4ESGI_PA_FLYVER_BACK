from dataclasses import Field
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

from app.models.modelplane import ModelPlane


class Seat(SQLModel, table=True):
    id_seat: Optional[int] = Field(default=None, primary_key=True)
    seat_number: str
    model_id: int = Field(foreign_key="modelplane.id_model")

    model: Optional[ModelPlane] = Relationship(back_populates="seats")
    reservations: List["Reservation"] = Relationship(back_populates="seat")