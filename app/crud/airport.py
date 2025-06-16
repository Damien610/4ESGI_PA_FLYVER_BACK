from __future__ import annotations

from sqlmodel import Session
from app.models.airport import Airport
from app.schemas.airport import AirportCreate, AirportUpdate

def create_airport(db: Session, data: AirportCreate) -> Airport:
    airport = Airport(**data.dict())
    db.add(airport)
    db.commit()
    db.refresh(airport)
    return airport

def get_airports(db: Session) -> list[Airport]:
    return db.query(Airport).all()

def get_airport_by_id(db: Session, id_airport: int) -> Airport | None:
    return db.get(Airport, id_airport)

def update_airport(db: Session, id_airport: int, data: AirportUpdate) -> Airport:
    airport = db.get(Airport, id_airport)
    if not airport:
        raise ValueError("Aéroport introuvable")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(airport, field, value)
    db.commit()
    db.refresh(airport)
    return airport

def delete_airport(db: Session, id_airport: int):
    airport = db.get(Airport, id_airport)
    if not airport:
        raise ValueError("Aéroport introuvable")

    db.delete(airport)
    db.commit()
