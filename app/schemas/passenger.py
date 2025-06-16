from pydantic import BaseModel
from datetime import date
from typing import Optional

class PassengerCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    nationality: str

class PassengerRead(PassengerCreate):
    id_passenger: int
    user_id: int

class PassengerUpdateModel(BaseModel):
    birth_date: Optional[date] = None
    nationality: Optional[str] = None
