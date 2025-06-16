from __future__ import annotations

from sqlmodel import Session, select
from app.models.modelplane import ModelPlane
from app.schemas.modelplane import ModelPlaneCreate, ModelPlaneUpdate

def create_model_plane(session: Session, model_data: ModelPlaneCreate) -> ModelPlane:
    model = ModelPlane(**model_data.dict())
    session.add(model)
    session.commit()
    session.refresh(model)
    return model

def get_model_plane(session: Session, model_id: int) -> ModelPlane | None:
    return session.get(ModelPlane, model_id)

def get_all_model_planes(session: Session) -> list[ModelPlane]:
    return session.exec(select(ModelPlane)).all()

def update_model_plane(session: Session, model_id: int, model_data: ModelPlaneUpdate) -> ModelPlane:
    model = session.get(ModelPlane, model_id)
    if not model:
        raise ValueError("Modèle non trouvé")

    for field, value in model_data.dict(exclude_unset=True).items():
        setattr(model, field, value)

    session.add(model)
    session.commit()
    session.refresh(model)
    return model

def delete_model_plane(session: Session, model_id: int) -> None:
    model = session.get(ModelPlane, model_id)
    if model:
        session.delete(model)
        session.commit()
