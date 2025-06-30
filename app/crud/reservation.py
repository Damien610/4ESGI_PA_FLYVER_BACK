from typing import List, Optional
from sqlmodel import Session, select
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate


def create_reservation(db: Session, data: ReservationCreate) -> Reservation:
    reservation = Reservation(**data.dict())
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation


def get_reservation_by_id(db: Session, reservation_id: int) -> Optional[Reservation]:
    return db.get(Reservation, reservation_id)


def get_all_reservations(db: Session) -> List[Reservation]:
    return db.exec(select(Reservation)).all()


def update_reservation(db: Session, reservation_id: int, data: ReservationUpdate) -> Reservation:
    reservation = db.get(Reservation, reservation_id)
    if not reservation:
        raise ValueError("Réservation introuvable")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(reservation, field, value)
    db.commit()
    db.refresh(reservation)
    return reservation


def delete_reservation(db: Session, reservation_id: int):
    reservation = db.get(Reservation, reservation_id)
    if not reservation:
        raise ValueError("Réservation introuvable")
    db.delete(reservation)
    db.commit()
