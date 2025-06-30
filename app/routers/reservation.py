from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import db
from app.schemas.reservation import ReservationCreate, ReservationUpdate, ReservationRead
from app.crud import reservation as crud

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("/", response_model=ReservationRead)
def create(data: ReservationCreate, db: Session = Depends(db.get_session)):
    return crud.create_reservation(db, data)


@router.get("/", response_model=List[ReservationRead])
def list_all(db: Session = Depends(db.get_session)):
    return crud.get_all_reservations(db)


@router.get("/{reservation_id}", response_model=ReservationRead)
def get_one(reservation_id: int, db: Session = Depends(db.get_session)):
    reservation = crud.get_reservation_by_id(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")
    return reservation


@router.put("/{reservation_id}", response_model=ReservationRead)
def update(reservation_id: int, data: ReservationUpdate, db: Session = Depends(db.get_session)):
    return crud.update_reservation(db, reservation_id, data)


@router.delete("/{reservation_id}")
def delete(reservation_id: int, db: Session = Depends(db.get_session)):
    crud.delete_reservation(db, reservation_id)
    return {"message": "Réservation supprimée"}
