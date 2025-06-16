from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import db
from app.models.user import User
from app.utils.security import get_current_user
from app.schemas.airport import AirportCreate, AirportRead, AirportUpdate
from app.crud.airport import (
    create_airport,
    get_airports,
    get_airport_by_id,
    update_airport,
    delete_airport
)

router = APIRouter(prefix="/airports", tags=["Airports"])

def admin_only(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    return user

@router.post("/", response_model=AirportRead)
def create(data: AirportCreate, session: Session = Depends(db.get_session), user: User = Depends(admin_only)):
    return create_airport(session, data)

@router.get("/", response_model=list[AirportRead])
def list_all(session: Session = Depends(db.get_session), user: User = Depends(admin_only)):
    return get_airports(session)

@router.get("/{airport_id}", response_model=AirportRead)
def get_one(airport_id: int, session: Session = Depends(db.get_session), user: User = Depends(admin_only)):
    airport = get_airport_by_id(session, airport_id)
    if not airport:
        raise HTTPException(status_code=404, detail="Aéroport introuvable")
    return airport

@router.put("/{airport_id}", response_model=AirportRead)
def update(
        airport_id: int,
        data: AirportUpdate,
        session: Session = Depends(db.get_session),
        user: User = Depends(admin_only)
):
    try:
        return update_airport(session, airport_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{airport_id}")
def delete(airport_id: int, session: Session = Depends(db.get_session), user: User = Depends(admin_only)):
    try:
        delete_airport(session, airport_id)
        return {"message": "Aéroport supprimé"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
