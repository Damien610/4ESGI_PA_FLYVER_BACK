from doctest import UnexpectedException
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import db
from app.crud.exception import NotFound
from app.crud.passenger import get_user_passengers, get_passenger_by_id, \
    create_passenger, update_passenger , delete_passenger
from app.models.passenger import Passenger
from app.schemas.passenger import PassengerCreate, PassengerRead, PassengerUpdateModel
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/passengers", tags=["Passengers"])


@router.post("/", response_model=PassengerRead)
def create_passenger_route(
        passenger: PassengerCreate,
        session: Session = Depends(db.get_session),
        current_user: User = Depends(get_current_user)
):
    return create_passenger(session, passenger, current_user)


@router.get("/", response_model=list[PassengerRead])
def list_my_passengers(
        session: Session = Depends(db.get_session),
        current_user: User = Depends(get_current_user)
):
    return get_user_passengers(current_user, session)



@router.get("/{passenger_id}", response_model=PassengerRead)
def get_my_passenger(
        passenger_id: int,
        session: Session = Depends(db.get_session),
        current_user: User = Depends(get_current_user)
):
    return get_passenger_by_id(passenger_id, current_user, session)


@router.put("/{passenger_id}", response_model=PassengerRead)
def update_my_passenger(
        passenger_id: int,
        data: PassengerUpdateModel,
        session: Session = Depends(db.get_session),
        current_user: User = Depends(get_current_user)
):
    return update_passenger(passenger_id, data, current_user, session)



@router.delete("/{passenger_id}")
def delete_my_passenger(
        passenger_id: int,
        session: Session = Depends(db.get_session),
        current_user: User = Depends(get_current_user)
):
    return delete_passenger(passenger_id, current_user, session)


