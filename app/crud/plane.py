from sqlmodel import Session
from app.models.plane import Plane
from app.schemas.plane import PlaneCreate, PlaneUpdate, PlaneRead
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

def create_plane(db: Session, plane_create: PlaneCreate) -> PlaneRead:
    try:
        plane = Plane.from_orm(plane_create)
        db.add(plane)
        db.commit()
        db.refresh(plane)
        return PlaneRead.from_orm(plane)
    except IntegrityError as e:
        db.rollback()
        # Optionnel : log e.orig ou str(e) pour debug
        raise HTTPException(status_code=400, detail="Foreign key constraint failed: model_id may not exist")

def get_all_planes(db: Session) -> list[PlaneRead]:
    planes = db.query(Plane).all()
    return [PlaneRead.from_orm(plane) for plane in planes]

def get_plane(plane_id: int, db: Session) -> PlaneRead:
    plane = db.get(Plane, plane_id)
    if not plane:
        raise HTTPException(status_code=404, detail="Plane not found")
    return PlaneRead.from_orm(plane)

def update_plane(plane_id: int, plane_update: PlaneUpdate, db: Session) -> PlaneRead:
    plane = db.get(Plane, plane_id)
    if not plane:
        raise HTTPException(status_code=404, detail="Plane not found")

    for field, value in plane_update.dict(exclude_unset=True).items():
        setattr(plane, field, value)

    db.add(plane)
    db.commit()
    db.refresh(plane)
    return PlaneRead.from_orm(plane)

def delete_plane(plane_id: int, db: Session):
    plane = db.get(Plane, plane_id)
    if not plane:
        raise HTTPException(status_code=404, detail="Plane not found")

    db.delete(plane)
    db.commit()
    return {"detail": "Plane deleted successfully"}