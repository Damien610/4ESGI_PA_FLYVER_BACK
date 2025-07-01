from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import db
from app.schemas.flight import FlightCreate, FlightUpdate, FlightRead
from app.crud.flight import (
    create_flight, get_flight_by_id, get_all_flights, update_flight, delete_flight
)

router = APIRouter(prefix="/flights", tags=["Flights"])


@router.post("/", response_model=FlightRead)
def create(data: FlightCreate, db: Session = Depends(db.get_session)):
    return create_flight(db, data)


@router.get("/", response_model=List[FlightRead])
def list_all(db: Session = Depends(db.get_session)):
    return get_all_flights(db)


@router.get("/{flight_id}", response_model=FlightRead)
def get_one(flight_id: int, db: Session = Depends(db.get_session)):
    return get_flight_by_id(db, flight_id)


@router.put("/{flight_id}", response_model=FlightRead)
def update(flight_id: int, data: FlightUpdate, db: Session = Depends(db.get_session)):
    return update_flight(db, flight_id, data)


@router.delete("/{flight_id}")
def remove(flight_id: int, db: Session = Depends(db.get_session)):
    return delete_flight(db, flight_id)
