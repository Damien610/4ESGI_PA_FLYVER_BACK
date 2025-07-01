
from typing import Type

from sqlmodel import Session

from app.crud.exception import NotFound, NotAuthorized, UnexpectedException
from app.models.user import User
from app.schemas.passenger import PassengerCreate
from app.models.passenger import Passenger
from app.schemas.passenger import PassengerUpdateModel
from fastapi import HTTPException

from app.utils.security import get_current_user


def create_passenger(db: Session, passenger_create: PassengerCreate, user: User) -> Passenger:

    data = passenger_create.dict()
    data["user_id"] = user.id_user
    passenger = Passenger(**data)
    db.add(passenger)
    db.commit()
    db.refresh(passenger)
    return passenger


def get_user_passengers(user: User, db: Session):
    users = db.query(Passenger).filter(Passenger.user_id == user.id_user).all()
    if not users:
        raise NotFound("No passengers found for this user")
    return users



def get_passenger_by_id(passenger_id: int, user: User, db: Session) -> Type[Passenger]:

    passenger = db.get(Passenger, passenger_id)

    if not passenger:
        raise NotFound("Passenger not found")

    if not user.is_admin and passenger.user_id != user.id_user:
        raise NotFound("Passenger not found")
    return passenger



def update_passenger(passenger_id: int, data: PassengerUpdateModel, user: User, db: Session) -> \
Type[Passenger]:
    passenger = db.get(Passenger, passenger_id)

    if not passenger:
        raise NotFound("Passenger not found")
    if passenger.user_id != user.id_user:
        raise NotFound("Passenger not found") #volontairement pas 403 pour ne pas leak l'existence

    for field, value in data.dict(exclude_unset=True).items():
        setattr(passenger, field, value)

    db.add(passenger)
    db.commit()
    db.refresh(passenger)
    return passenger



def delete_passenger(passenger_id: int, user: User, db: Session):

    passenger = db.get(Passenger, passenger_id)
    if not passenger:
        raise NotFound("Passenger not found")
    if passenger.user_id != user.id_user:
        raise NotFound("Passenger not found")

    db.delete(passenger)
    db.commit()
    return {"detail": "Passenger deleted successfully"}

