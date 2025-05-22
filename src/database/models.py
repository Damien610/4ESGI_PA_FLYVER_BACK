from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


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