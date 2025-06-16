# app/crud/passenger.py
from sqlmodel import Session
from app.models.passenger import Passenger
from app.schemas.passenger import PassengerCreate
from app.models.passenger import Passenger
from app.schemas.passenger import PassengerUpdateModel
from fastapi import HTTPException


def create_passenger(db: Session, passenger_create: PassengerCreate, user_id: int) -> Passenger:
    data = passenger_create.dict()
    data["user_id"] = user_id
    passenger = Passenger(**data)
    db.add(passenger)
    db.commit()
    db.refresh(passenger)
    return passenger


def get_user_passengers(user_id: int, db: Session):
    return db.query(Passenger).filter(Passenger.user_id == user_id).all()

def update_passenger(passenger_id: int, data: PassengerUpdateModel, user_id: int, db: Session) -> Passenger:
    passenger = db.get(Passenger, passenger_id)
    if not passenger or passenger.user_id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé ou passager inexistant")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(passenger, field, value)

    db.add(passenger)
    db.commit()
    db.refresh(passenger)
    return passenger

def delete_passenger(passenger_id: int, user_id: int, db: Session):
    passenger = db.get(Passenger, passenger_id)
    if not passenger or passenger.user_id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé ou passager inexistant")

    db.delete(passenger)
    db.commit()

