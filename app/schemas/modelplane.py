from __future__ import annotations

from pydantic import BaseModel

class ModelPlaneBase(BaseModel):
    name: str
    manufacturer: str
    capacity: int = 0

class ModelPlaneCreate(ModelPlaneBase):
    pass

class ModelPlaneRead(ModelPlaneBase):
    id_model: int

    class Config:
        from_attributes = True

class ModelPlaneUpdate(BaseModel):
    name: str | None = None
    manufacturer: str | None = None
    capacity: int | None = None
