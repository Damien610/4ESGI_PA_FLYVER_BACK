from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import db
from app.models.user import User
from app.schemas.modelplane import ModelPlaneCreate, ModelPlaneRead, ModelPlaneUpdate
from app.crud.modelplane import (
    create_model_plane, get_all_model_planes, get_model_plane,
    update_model_plane, delete_model_plane
)
from app.utils.security import get_current_user

router = APIRouter(prefix="/model-planes", tags=["Model Planes"])

def require_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    return user

@router.post("/", response_model=ModelPlaneRead)
def create(model: ModelPlaneCreate, session: Session = Depends(db.get_session), _: User = Depends(require_admin)):
    return create_model_plane(session, model)

@router.get("/", response_model=list[ModelPlaneRead])
def list_all(session: Session = Depends(db.get_session)):
    return get_all_model_planes(session)

@router.get("/{model_id}", response_model=ModelPlaneRead)
def read(model_id: int, session: Session = Depends(db.get_session)):
    model = get_model_plane(session, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    return model

@router.put("/{model_id}", response_model=ModelPlaneRead)
def update(model_id: int, data: ModelPlaneUpdate, session: Session = Depends(db.get_session), _: User = Depends(require_admin)):
    try:
        return update_model_plane(session, model_id, data)
    except ValueError:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")

@router.delete("/{model_id}")
def delete(model_id: int, session: Session = Depends(db.get_session), _: User = Depends(require_admin)):
    delete_model_plane(session, model_id)
    return {"detail": "Modèle supprimé"}
