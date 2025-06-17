from pydantic import BaseModel
from datetime import date
from typing import Optional

class PlaneCreate(BaseModel):
    registration: str
    model_id: int

class PlaneRead(PlaneCreate):
    id_plane: int
    registration: str
    model_id: int

    class Config:
        from_attributes = True

class Plane(BaseModel):
    id_plane: int
    registration: str
    model_id: int

class PlaneUpdate(BaseModel):
    registration: Optional[str] = None
    model_id: Optional[int] = None