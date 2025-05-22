from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import UniqueConstraint

# === USERS ===
class User(SQLModel, table=True):
    __tablename__ = "users"

    id_users: Optional[int] = Field(default=None, primary_key=True)
    name: str
    first_name: str
    email: str
    is_admin: Optional[bool] = Field(default=False)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# === RefreshToken ===
class RefreshToken(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    token: str
    user_id: int
    expires_at: datetime

# === Airport ===
class Airport(SQLModel, table=True):
    __tablename__ = "airports"
    __table_args__ = (
        UniqueConstraint("name", name="uq_airport_name"),
        UniqueConstraint("iata", name="uq_airport_iata"),
    )
    id_airport: Optional[int] = Field(default=None, primary_key=True)
    name: str
    iata: str
    city: str
    country: str
    created_at: datetime = Field(default_factory=datetime.utcnow)