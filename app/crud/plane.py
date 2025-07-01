from sqlmodel import Session
from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError

from app.crud.exception import NotFound
from app.models.plane import Plane
from app.schemas.plane import PlaneCreate, PlaneUpdate, PlaneRead


def create_plane(db: Session, plane_create: PlaneCreate) -> PlaneRead:
    try:
        plane = Plane.from_orm(plane_create)
        db.add(plane)
        db.commit()
        db.refresh(plane)
        return PlaneRead.from_orm(plane)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Foreign key constraint failed: model_id may not exist"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while creating plane: {e}"
        )


def get_all_planes(db: Session) -> list[PlaneRead]:
    try:
        planes = db.query(Plane).all()
        return [PlaneRead.from_orm(plane) for plane in planes]
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while fetching planes: {e}"
        )


def get_plane(plane_id: int, db: Session) -> PlaneRead:
    try:
        plane = db.get(Plane, plane_id)
        if not plane:
            raise NotFound("Plane not found")
        return PlaneRead.from_orm(plane)
    except NotFound as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while fetching plane: {e}"
        )


def update_plane(plane_id: int, plane_update: PlaneUpdate, db: Session) -> PlaneRead:
    try:
        plane = db.get(Plane, plane_id)
        if not plane:
            raise NotFound("Plane not found")

        for field, value in plane_update.dict(exclude_unset=True).items():
            setattr(plane, field, value)

        db.add(plane)
        db.commit()
        db.refresh(plane)
        return PlaneRead.from_orm(plane)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Foreign key constraint failed during update"
        )
    except NotFound as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while updating plane: {e}"
        )


def delete_plane(plane_id: int, db: Session):
    try:
        plane = db.get(Plane, plane_id)
        if not plane:
            raise NotFound("Plane not found")

        db.delete(plane)
        db.commit()
        return {"detail": "Plane deleted successfully"}
    except NotFound as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while deleting plane: {e}"
        )
