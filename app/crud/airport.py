from __future__ import annotations

from doctest import UnexpectedException
from http.client import HTTPException
from json import loads
from logging import exception

from sqlmodel import Session

from app.core.minio_client import upload_image_to_minio, delete_image_from_minio
from app.crud.exception import BadRequest, AlreadyExist, NotFound
from app.models.airport import Airport
from app.schemas.airport import AirportCreate, AirportUpdate
from fastapi import UploadFile
from typing import List, Type


def create_airport(db: Session, data: AirportCreate, images: List[UploadFile]) -> Airport:
    image_urls = []

    if not (isinstance(data.iata, str) and len(data.iata) == 3 and data.iata.isupper()):
        raise BadRequest("IATA code must be a 3-letter uppercase string.")

    existing_airport = db.query(Airport).filter_by(iata=data.iata).first()
    if existing_airport:
        raise AlreadyExist("An airport with this IATA code already exists.")

    image_urls = [upload_image_to_minio(file) for file in images] if images else []
    data.image_urls = image_urls

    airport = Airport(**data.dict(exclude_unset=True, exclude={"image_urls"}))
    airport.set_image_urls(image_urls if isinstance(image_urls, list) else [])

    db.add(airport)
    db.commit()
    db.refresh(airport)

    return airport



def get_airports(db: Session) -> list[Airport]:

    airports = db.query(Airport).all()
    if not airports:
        raise NotFound("No airports found")
    for airport in airports:
        if isinstance(airport.image_urls, str):
            airport.image_urls = loads(airport.image_urls)
    return airports




def get_airport_by_id(db: Session, id_airport: int) -> Type[Airport]:
    airport = db.get(Airport, id_airport)
    if not airport:
        raise NotFound("Airport not found")
    if airport and isinstance(airport.image_urls, str):
        airport.image_urls = loads(airport.image_urls)
    return airport


def update_airport(db: Session, id_airport: int, data: AirportUpdate, images: List[UploadFile]) -> Airport:
    airport = db.get(Airport, id_airport)
    if not airport:
        raise NotFound("Airport not found")

    if data.iata and (not isinstance(data.iata, str) or len(data.iata) != 3 or not data.iata.isupper()):
        raise BadRequest("IATA code must be a 3-letter uppercase string.")

    if data.iata and data.iata != airport.iata:
        existing_airport = db.query(Airport).filter_by(iata=data.iata).first()
        if existing_airport:
            raise AlreadyExist("An airport with this IATA code already exists.")


    if data.image_urls:
        image_urls = [upload_image_to_minio(file) for file in images]
        data.image_urls = image_urls

    airport_data = {
        k: v for k, v in data.dict(exclude_unset=True, exclude={"image_urls"}).items()
        if v is not None
    }
    for key, value in airport_data.items():
        setattr(airport, key, value)

    db.add(airport)
    db.commit()
    db.refresh(airport)

    return airport

def delete_airport(db: Session, id_airport: int):

    airport = db.get(Airport, id_airport)
    if not airport:
        raise NotFound("Airport not found")
    if isinstance(airport.image_urls, str):
        image_urls = loads(airport.image_urls)
        for url in image_urls:
            try:
                delete_image_from_minio(url)
            except Exception as e:
                print(f"Error while deleting image {url}: {e}")
    db.delete(airport)
    db.commit()
    return {"message": "Airport deleted successfully"}
