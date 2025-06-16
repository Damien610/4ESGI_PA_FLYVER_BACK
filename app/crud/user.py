from __future__ import annotations

from typing import Type

from sqlmodel import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdateModel
from app.core.config import settings
import hmac
import hashlib

def hash_password(password: str) -> str:
    return hmac.new(
        key=settings.secret_key.encode(),
        msg=password.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

def create_user(db: Session, user_create: UserCreate) -> User:
    existing_user = db.query(User).filter(User.email == user_create.email).first()
    if existing_user:
        raise ValueError("Un utilisateur avec cet email existe déjà.")

    user_data = user_create.dict()
    user_data["password_hash"] = hash_password(user_create.password_hash)
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)

def get_users(db: Session) -> list[User]:
    return db.query(User).all()

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def update_user(user_id: int, user_data: UserUpdateModel, db: Session) -> Type[User]:
    db_user = db.get(User, user_id)
    if not db_user:
        raise ValueError("Utilisateur introuvable")

    updates = user_data.dict(exclude_unset=True)

    if "email" in updates:
        existing = db.query(User).filter(User.email == updates["email"]).first()
        if existing and existing.id_user != user_id:
            raise ValueError("Cet email est déjà utilisé par un autre utilisateur.")

    for field, value in updates.items():
        setattr(db_user, field, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
