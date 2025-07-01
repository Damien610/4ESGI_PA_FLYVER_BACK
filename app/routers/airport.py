from doctest import UnexpectedException
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlmodel import Session
from typing import List, Optional
from app.core.database import db
from app.crud.exception import NotFound, AlreadyExist, BadRequest
from app.utils.security import admin_only
from app.schemas.airport import AirportCreate,AirportRead, AirportUpdate
from app.crud.airport import (
    create_airport,
    get_airports,
    get_airport_by_id,
    update_airport,
    delete_airport
)


router = APIRouter(
    prefix="/airports",
    tags=["Airports"],
    dependencies=[Depends(admin_only)]
)

@router.post("/", response_model=AirportRead)
def create_airport_endpoint(
        name: str = Form(..., example="Charles de Gaulle"),
        iata: str = Form(..., example="CDG"),
        city: str = Form(..., example="Paris"),
        country: str = Form(..., example="France"),
        images: Optional[List[UploadFile]] = File(default_factory=list),
        session: Session = Depends(db.get_session)
):
    data = AirportCreate(name=name, iata=iata, city=city, country=country)
    airport = create_airport(session, data, images=images or [])
    airport.image_urls= airport.get_image_urls()
    return airport



@router.get("/", response_model=List[AirportRead])
def list_all(session: Session = Depends(db.get_session)):
    return get_airports(session)



@router.get("/{airport_id}", response_model=AirportRead)
def get_one(airport_id: int, session: Session = Depends(db.get_session)):
    return get_airport_by_id(session, airport_id)


@router.put("/{airport_id}", response_model=AirportRead)
def update(airport_id: int,
           name: Optional[str] = Form(None, example="Charles de Gaulle"),
           iata: Optional[str] = Form(None, example="CDG"),
           city: Optional[str] = Form(None, example="Paris"),
           country: Optional[str] = Form(None, example="France"),
           images: Optional[List[UploadFile]] = File(default_factory=list),
           session: Session = Depends(db.get_session)):

    data = AirportUpdate(name=name, iata=iata, city=city, country=country)
    airport = update_airport(session,airport_id, data, images=images or [])
    airport.image_urls= airport.get_image_urls()
    return airport


@router.delete("/{airport_id}")
def delete(airport_id: int, session: Session = Depends(db.get_session)):
    return delete_airport(session, airport_id)

