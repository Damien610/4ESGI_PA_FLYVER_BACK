from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import db
from app.models.passenger import Passenger
from app.schemas.passenger import PassengerCreate, PassengerRead, PassengerUpdateModel
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/passengers", tags=["Passengers"])

# ✅ Créer un passager pour l'utilisateur connecté
@router.post("/", response_model=PassengerRead)
def create_passenger_route(
        passenger: PassengerCreate,
        session: Session = Depends(db.get_session),
        current_user: User = Depends(get_current_user)
):
    new_passenger = Passenger(**passenger.dict(), user_id=current_user.id_user)
    session.add(new_passenger)
    session.commit()
    session.refresh(new_passenger)
    return new_passenger

# ✅ Lister uniquement les passagers de l'utilisateur
@router.get("/", response_model=list[PassengerRead])
def list_my_passengers(
        session: Session = Depends(db.get_session),
        current_user: User = Depends(get_current_user)
):
    return session.query(Passenger).filter(Passenger.user_id == current_user.id_user).all()

# ✅ Voir un seul passager uniquement s'il t'appartient
@router.get("/{passenger_id}", response_model=PassengerRead)
def get_my_passenger(
        passenger_id: int,
        session: Session = Depends(db.get_session),
        current_user: User = Depends(get_current_user)
):
    passenger = session.get(Passenger, passenger_id)
    if not passenger or passenger.user_id != current_user.id_user:
        raise HTTPException(status_code=404, detail="Passager non trouvé")
    return passenger

# ✅ Modifier son propre passager
@router.put("/{passenger_id}", response_model=PassengerRead)
def update_my_passenger(
        passenger_id: int,
        data: PassengerUpdateModel,
        session: Session = Depends(db.get_session),
        current_user: User = Depends(get_current_user)
):
    passenger = session.get(Passenger, passenger_id)
    if not passenger or passenger.user_id != current_user.id_user:
        raise HTTPException(status_code=403, detail="Accès interdit")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(passenger, field, value)
    session.commit()
    session.refresh(passenger)
    return passenger

# ✅ Supprimer son propre passager
@router.delete("/{passenger_id}")
def delete_my_passenger(
        passenger_id: int,
        session: Session = Depends(db.get_session),
        current_user: User = Depends(get_current_user)
):
    passenger = session.get(Passenger, passenger_id)
    if not passenger or passenger.user_id != current_user.id_user:
        raise HTTPException(status_code=403, detail="Accès interdit")

    session.delete(passenger)
    session.commit()
    return {"message": "Passager supprimé"}
