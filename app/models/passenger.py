from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import date

class Passenger(SQLModel, table=True):
    __tablename__ = "passengers"

    id_passenger: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    birth_date: date
    nationality: str
    gender: Optional[str] = None  # Nouveau champ
    user_id: int = Field(foreign_key="users.id_user")

    reservations: List["Reservation"] = Relationship(back_populates="passenger")