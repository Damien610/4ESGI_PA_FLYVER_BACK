from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session,select

from pydantic import BaseModel
import hashlib
from jose import jwt, JWTError
from datetime import datetime, timedelta
from jose.exceptions import ExpiredSignatureError

from fastapi import Header, status
import secrets
from database.connection import db
from database.models import User, RefreshToken
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()

from HTTP_Models.MOD_auth import UserCreate, UserLogin


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/register", tags=["Authentification"])
def register(user: UserCreate, session: Session = Depends(db.get_session)):
    existing = session.exec(
        select(User).where(User.email == user.email)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Cet utilisateur existe déjà.")

    hashed_pwd = hash_password(user.password)
    new_user = User(email=user.email, password_hash=hashed_pwd, is_admin=user.is_admin,first_name=user.first_name,name=user.name)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {
        "message": "Utilisateur créé avec succès.",
        "user_id": new_user.id_users
    }


SECRET_KEY = "supersecretclépourlesjetons"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


@router.post("/login", tags=["Authentification"])
def login(user: UserLogin, session: Session = Depends(db.get_session)):
    db_user = session.exec(
        select(User).where(User.email == user.email)
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")

    hashed_pwd = hash_password(user.password)
    if db_user.password_hash != hashed_pwd:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")

    # Générer le token d'accès
    token_data = {
        "sub": db_user.email,
        "name": db_user.name,
        "first_name": db_user.first_name,
        "is_admin": db_user.is_admin,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    # Générer le refresh token
    refresh_token = secrets.token_hex(32)
    refresh_token_expiration = datetime.utcnow() + timedelta(days=30)

    # Sauvegarder le refresh token dans la base de données
    new_refresh_token = RefreshToken(
        token=refresh_token,
        user_id=db_user.id_users,
        expires_at=refresh_token_expiration
    )
    session.add(new_refresh_token)
    session.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", tags=["Authentification"])
def get_current_user(token: str = Depends(oauth2_scheme)):
    print("Token reçu :", token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "email": payload.get("sub"),
            "first_name": payload.get("first_name"),
            "name": payload.get("name"),
            "role": payload.get("is_admin"),
        }
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Le token a expiré"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )


@router.post("/refresh", tags=["Authentification"])
def refresh_token(refresh_token: str, session: Session = Depends(db.get_session)):
    # Vérifier si le refresh token est valide
    db_refresh_token = session.exec(
        select(RefreshToken).where(RefreshToken.token == refresh_token)
    ).first()

    if not db_refresh_token or db_refresh_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token invalide ou expiré.")

    # Récupérer l'utilisateur associé
    db_user = session.exec(
        select(User).where(User.id_users == db_refresh_token.user_id)
    ).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    # Générer un nouveau token d'accès
    token_data = {
        "sub": db_user.email,
        "name": db_user.name,
        "first_name": db_user.first_name,
        "is_admin": db_user.is_admin,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}