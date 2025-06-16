from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.core.database import db
from app.crud.user import get_user_by_email, hash_password
from app.utils.security import create_access_token, create_refresh_token, verify_token
from jose import JWTError

router = APIRouter(prefix="/auth", tags=["Authentification"])

# Déjà présent :
@router.post("/login")
def login(
        email: str = Form(...),
        password: str = Form(...),
        session: Session = Depends(db.get_session)
):
    user = get_user_by_email(session, email)
    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe invalide")

    if user.password_hash != hash_password(password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe invalide")

    access_token = create_access_token({"sub": str(user.id_user)})
    refresh_token = create_refresh_token({"sub": str(user.id_user)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# 🔄 Refresh
@router.post("/refresh")
def refresh_token(refresh_token: str = Form(...)):
    try:
        payload = verify_token(refresh_token)
        if not payload:
            raise HTTPException(status_code=401, detail="Token invalide")
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token invalide")
        new_access_token = create_access_token({"sub": str(user_id)})
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

from app.utils.security import get_current_user
from app.models.user import User

@router.get("/me", response_model=User)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
