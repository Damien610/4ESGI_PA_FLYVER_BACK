from typing import List, Optional
from sqlmodel import Session, select
from app.models.flight import Flight
from app.schemas.flight import FlightCreate, FlightUpdate


def create_flight(db: Session, data: FlightCreate) -> Flight:
    flight = Flight(**data.dict())
    db.add(flight)
    db.commit()
    db.refresh(flight)
    return flight


def get_flight_by_id(db: Session, flight_id: int) -> Optional[Flight]:
    return db.get(Flight, flight_id)


def get_all_flights(db: Session) -> List[Flight]:
    return db.exec(select(Flight)).all()


def update_flight(db: Session, flight_id: int, data: FlightUpdate) -> Flight:
    flight = db.get(Flight, flight_id)
    if not flight:
        raise ValueError("Vol introuvable")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(flight, field, value)
    db.commit()
    db.refresh(flight)
    return flight


def delete_flight(db: Session, flight_id: int):
    flight = db.get(Flight, flight_id)
    if not flight:
        raise ValueError("Vol introuvable")
    db.delete(flight)
    db.commit()
