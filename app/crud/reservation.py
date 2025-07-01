from typing import List
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate
from app.crud.exception import NotFound, UnexpectedException


def create_reservation(db: Session, data: ReservationCreate) -> Reservation:
    try:
        reservation = Reservation(**data.dict())
        db.add(reservation)
        db.commit()
        db.refresh(reservation)
        return reservation
    except IntegrityError:
        db.rollback()
        raise UnexpectedException("Reservation creation failed due to foreign key or constraint error")
    except Exception as e:
        db.rollback()
        raise UnexpectedException(f"Unexpected error while creating reservation: {str(e)}")


def get_reservation_by_id(db: Session, reservation_id: int) -> Reservation:
    try:
        reservation = db.get(Reservation, reservation_id)
        if not reservation:
            raise NotFound("Reservation not found")
        return reservation
    except Exception as e:
        raise UnexpectedException(f"Unexpected error while fetching reservation: {str(e)}")


def get_all_reservations(db: Session) -> List[Reservation]:
    try:
        return db.exec(select(Reservation)).all()
    except Exception as e:
        raise UnexpectedException(f"Unexpected error while listing reservations: {str(e)}")


def update_reservation(db: Session, reservation_id: int, data: ReservationUpdate) -> Reservation:
    try:
        reservation = db.get(Reservation, reservation_id)
        if not reservation:
            raise NotFound("Reservation not found")
        for field, value in data.dict(exclude_unset=True).items():
            setattr(reservation, field, value)
        db.commit()
        db.refresh(reservation)
        return reservation
    except IntegrityError:
        db.rollback()
        raise UnexpectedException("Update failed due to constraint violation")
    except Exception as e:
        db.rollback()
        raise UnexpectedException(f"Unexpected error while updating reservation: {str(e)}")


def delete_reservation(db: Session, reservation_id: int):
    try:
        reservation = db.get(Reservation, reservation_id)
        if not reservation:
            raise NotFound("Reservation not found")
        db.delete(reservation)
        db.commit()
        return {"message": "Reservation deleted successfully"}
    except Exception as e:
        db.rollback()
        raise UnexpectedException(f"Unexpected error while deleting reservation: {str(e)}")
