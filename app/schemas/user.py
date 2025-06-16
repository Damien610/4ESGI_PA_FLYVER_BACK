from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    first_name: str
    email: str
    password_hash: str
    is_admin: bool = False

class UserRead(BaseModel):
    id_user: int
    name: str
    first_name: str
    email: str
    is_admin: bool
    created_at: datetime

    class Config:
        orm_mode = True

class UserUpdateModel(BaseModel):
    name: Optional[str] = None
    first_name: Optional[str] = None
    email: Optional[str] = None
    is_admin: Optional[bool] = None