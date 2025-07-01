from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.models.flight import Flight
from app.schemas.flight import FlightCreate, FlightUpdate
from app.crud.exception import NotFound, UnexpectedException


def create_flight(db: Session, data: FlightCreate) -> Flight:
    try:
        flight = Flight(**data.dict())
        db.add(flight)
        db.commit()
        db.refresh(flight)
        return flight
    except IntegrityError:
        db.rollback()
        raise UnexpectedException("Flight creation failed due to constraint violation")
    except Exception as e:
        db.rollback()
        raise UnexpectedException(f"Unexpected error while creating flight: {str(e)}")


def get_flight_by_id(db: Session, flight_id: int) -> Flight:
    try:
        flight = db.get(Flight, flight_id)
        if not flight:
            raise NotFound("Flight not found")
        return flight
    except Exception as e:
        raise UnexpectedException(f"Unexpected error while fetching flight: {str(e)}")


def get_all_flights(db: Session) -> List[Flight]:
    try:
        return db.exec(select(Flight)).all()
    except Exception as e:
        raise UnexpectedException(f"Unexpected error while listing flights: {str(e)}")


def update_flight(db: Session, flight_id: int, data: FlightUpdate) -> Flight:
    try:
        flight = db.get(Flight, flight_id)
        if not flight:
            raise NotFound("Flight not found")
        for field, value in data.dict(exclude_unset=True).items():
            setattr(flight, field, value)
        db.commit()
        db.refresh(flight)
        return flight
    except IntegrityError:
        db.rollback()
        raise UnexpectedException("Update failed due to constraint violation")
    except Exception as e:
        db.rollback()
        raise UnexpectedException(f"Unexpected error while updating flight: {str(e)}")


def delete_flight(db: Session, flight_id: int):
    try:
        flight = db.get(Flight, flight_id)
        if not flight:
            raise NotFound("Flight not found")
        db.delete(flight)
        db.commit()
        return {"message": "Flight deleted successfully"}
    except Exception as e:
        db.rollback()
        raise UnexpectedException(f"Unexpected error while deleting flight: {str(e)}")
