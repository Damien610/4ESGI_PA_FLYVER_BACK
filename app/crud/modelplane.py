from __future__ import annotations

from typing import Sequence, Type, Dict

from sqlmodel import Session, select

from app.crud.exception import NotFound
from app.models.modelplane import ModelPlane
from app.schemas.modelplane import ModelPlaneCreate, ModelPlaneUpdate

def create_model_plane(session: Session, model_data: ModelPlaneCreate) -> ModelPlane:
    model = ModelPlane(**model_data.dict())
    session.add(model)
    session.commit()
    session.refresh(model)
    return model

def get_model_plane(session: Session, model_id: int) -> Type[ModelPlane]:
    model = session.get(ModelPlane, model_id)
    if not model:
        raise NotFound("Plane model not found")
    return model

def get_all_model_planes(session: Session) -> Sequence[ModelPlane]:
    models = session.exec(select(ModelPlane)).all()
    if not models:
        raise NotFound("No plane models found")
    return models

def update_model_plane(session: Session, model_id: int, model_data: ModelPlaneUpdate) -> \
Type[ModelPlane]:
    model = session.get(ModelPlane, model_id)
    if not model:
        raise NotFound("Plane model not found")

    for field, value in model_data.dict(exclude_unset=True).items():
        setattr(model, field, value)

    session.add(model)
    session.commit()
    session.refresh(model)
    return model

def delete_model_plane(session: Session, model_id: int) -> dict[str, str]:
    model = session.get(ModelPlane, model_id)
    if model:
        session.delete(model)
        session.commit()
        return {"message": "Plane model deleted successfully"}
    else:
        raise NotFound("Plane model not found")