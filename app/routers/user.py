from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdateModel
from app.crud.user import create_user, get_users, update_user, get_user_by_id
from app.utils.security import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead)
def register_user(user: UserCreate, session: Session = Depends(db.get_session)):
    try:
        return create_user(session, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[UserRead])
def list_users(session: Session = Depends(db.get_session)):
    return get_users(session)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(db.get_session)):
    user = get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


@router.put("/{user_id}", response_model=User)
def update_user_route(
        user_id: int,
        user_data: UserUpdateModel,
        session: Session = Depends(db.get_session),
        current_user: User = Depends(get_current_user)  # ← Importe le user depuis le token JWT
):
    if current_user.id_user != user_id:
        raise HTTPException(status_code=403, detail="Modification non autorisée")

    try:
        return update_user(user_id, user_data, session)
    except ValueError:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

