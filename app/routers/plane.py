from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import db
from app.crud.plane import create_plane, get_all_planes, delete_plane,get_plane, update_plane
from app.schemas.plane import PlaneCreate, PlaneUpdate, PlaneRead
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/planes", tags=["Planes"])

def require_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    return user

@router.post("/", response_model=PlaneRead)
def create(model: PlaneCreate, session: Session = Depends(db.get_session), _: User = Depends(require_admin)):
    return create_plane(session, model)

@router.get("/", response_model=list[PlaneRead])
def list_all(session: Session = Depends(db.get_session)):
    return get_all_planes(session)

@router.get("/{plane_id}", response_model=PlaneRead)
def read(plane_id: int, session: Session = Depends(db.get_session)):
    model = get_plane(plane_id,session)
    if not model:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    return model

@router.put("/{plane_id}", response_model=PlaneRead)
def update(plane_id: int, data: PlaneUpdate, session: Session = Depends(db.get_session), _: User = Depends(require_admin)):
    try:
        return update_plane(plane_id, data, session)
    except ValueError:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")

@router.delete("/{plane_id}")
def delete(plane_id: int, session: Session = Depends(db.get_session), _: User = Depends(require_admin)):
    delete_plane(plane_id,session)
    return {"detail": "Modèle supprimé"}