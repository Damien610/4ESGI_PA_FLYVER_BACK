from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import ExpiredSignatureError
from pydantic import BaseModel
from database.connection import db
from database.models import Airport, RefreshToken
from typing import Optional
from sqlmodel import Session,select
from fastapi import Query

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()

class AirportCreateModel(BaseModel):
    name: str
    iata: str
    city: str
    country: str

class AirportUpdateModel(BaseModel):
    name: Optional[str] = None
    iata: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

@router.put("/airport", tags=["Aéroports"])
def put_plane(airport: AirportCreateModel, token: str = Depends(oauth2_scheme), session: Session = Depends(db.get_session)):
    if len(airport.iata) != 3:
        raise HTTPException(status_code=400, detail="L'IATA doit faire 3 caractères.")

    # Vérification unicité
    existing = session.exec(
        select(Airport).where((Airport.name == airport.name) | (Airport.iata == airport.iata))
    ).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Un aéroport avec ce nom ou ce code IATA existe déjà."
        )

    new_airport = Airport(name=airport.name, iata=airport.iata, city=airport.city, country=airport.country)
    session.add(new_airport)
    session.commit()
    session.refresh(new_airport)
    return {
        "message": "Aéroport créé avec succès.",
        "airport_id": new_airport.id_airport
    }

@router.get("/airport", tags=["Aéroports"])
def get_airport(
        id: Optional[int] = Query(None, description="ID de l'aéroport"),
        name: Optional[str] = Query(None, description="Nom de l'aéroport"),
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(db.get_session)
):
    if id:
        airport = session.exec(select(Airport).where(Airport.id_airport == id)).first()
        if not airport:
            raise HTTPException(status_code=404, detail="Aucun aéroport trouvé avec cet ID.")
        return {
            "airport": airport
        }
    elif name:
        airports = session.exec(select(Airport).where(Airport.name.ilike(f"%{name}%"))).all()
        if not airports:
            raise HTTPException(status_code=404, detail="Aucun aéroport trouvé avec ce nom.")
        return {
            "airports": airports
        }
    else:
        airports = session.exec(select(Airport)).all()
        if not airports:
            raise HTTPException(status_code=404, detail="Aucun aéroport trouvé.")
        return {
            "airports": airports
        }

@router.delete("/airport", tags=["Aéroports"])
def delete_airport(
        id: Optional[int] = Query(None, description="ID de l'aéroport"),
        name: Optional[str] = Query(None, description="Nom de l'aéroport"),
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(db.get_session)
):
    if id:
        airport = session.exec(select(Airport).where(Airport.id_airport == id)).first()
        if not airport:
            raise HTTPException(status_code=404, detail="Aucun aéroport trouvé avec cet ID.")
    elif name:
        airport = session.exec(select(Airport).where(Airport.name.ilike(f"%{name}%"))).first()
        if not airport:
            raise HTTPException(status_code=404, detail="Aucun aéroport trouvé avec ce nom.")
    else:
        raise HTTPException(status_code=400, detail="Veuillez fournir un ID ou un nom d'aéroport.")

    session.delete(airport)
    session.commit()

    return {"message": f"L'aéroport '{airport.name}' a été supprimé avec succès."}

@router.patch("/airport", tags=["Aéroports"])
def update_airport(
        id: int = Query(..., description="ID de l'aéroport à modifier"),
        airport_update: AirportUpdateModel = ...,  # données à mettre à jour
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(db.get_session)
):
    airport = session.exec(select(Airport).where(Airport.id_airport == id)).first()
    if not airport:
        raise HTTPException(status_code=404, detail="Aucun aéroport trouvé avec cet ID.")

    if airport_update.name and airport_update.name != airport.name:
        existing_name = session.exec(
            select(Airport).where(Airport.name == airport_update.name)
        ).first()
        if existing_name:
            raise HTTPException(status_code=409, detail="Ce nom d'aéroport existe déjà.")

    if airport_update.iata:
        if len(airport_update.iata) != 3:
            raise HTTPException(status_code=400, detail="L'IATA doit faire 3 caractères.")
        if airport_update.iata != airport.iata:
            existing_iata = session.exec(
                select(Airport).where(Airport.iata == airport_update.iata)
            ).first()
            if existing_iata:
                raise HTTPException(status_code=409, detail="Ce code IATA existe déjà.")

    # Mise à jour des champs
    for field, value in airport_update.dict(exclude_unset=True).items():
        setattr(airport, field, value)

    session.add(airport)
    session.commit()
    session.refresh(airport)

    return {
        "message": f"Aéroport '{airport.name}' mis à jour avec succès.",
        "airport": airport
    }

