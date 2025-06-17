from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

from app.models.modelplane import ModelPlane


class Plane(SQLModel, table=True):
    id_plane: Optional[int] = Field(default=None, primary_key=True)
    registration: str
    model_id: int = Field(foreign_key="modelplane.id_model")

    model: Optional[ModelPlane] = Relationship(back_populates="planes")
    flights: List["Flight"] = Relationship(back_populates="plane")