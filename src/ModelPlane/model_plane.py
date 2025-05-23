from fastapi import APIRouter, Depends, HTTPException, Query
from database.connection import db
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from typing import Optional, List
from HTTP_Models.MOD_Model_Plane import ModeleCreateModels, ModeleUpdateModel
from database.models import ModelPlane

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()

@router.put("/model_plane", tags=["Modèles d'avion"])
def put_model_plane(
        model_plane: ModeleCreateModels,
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(db.get_session)
):
    existing = session.exec(
        select(ModelPlane).where(
            (ModelPlane.name == model_plane.name) &
            (ModelPlane.manufacturer == model_plane.manufacturer)
        )
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Un modèle d'avion avec ce nom et ce constructeur existe déjà."
        )

    new_model_plane = ModelPlane(
        name=model_plane.name,
        manufacturer=model_plane.manufacturer,
        capacity=model_plane.capacity
    )
    session.add(new_model_plane)
    session.commit()
    session.refresh(new_model_plane)

    return {
        "message": "Modèle d'avion créé avec succès.",
        "model_plane_id": new_model_plane.id_model_plane
    }

@router.get("/model_plane", tags=["Modèles d'avion"])
def get_model_planes(
        name: Optional[str] = Query(None),
        manufacturer: Optional[str] = Query(None),
        id: Optional[int] = Query(None),
        session: Session = Depends(db.get_session)
) -> List[ModelPlane]:
    query = select(ModelPlane)

    if name:
        query = query.where(ModelPlane.name == name)
    if manufacturer:
        query = query.where(ModelPlane.manufacturer == manufacturer)
    if id:
        query = query.where(ModelPlane.id_model_plane == id)

    results = session.exec(query).all()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="Aucun modèle d'avion trouvé avec les critères spécifiés."
        )

    return results


@router.patch("/model_plane/{model_plane_id}", tags=["Modèles d'avion"])
def update_model_plane(
        model_plane_id: int,
        update_data: ModeleUpdateModel,
        session: Session = Depends(db.get_session),
        token: str = Depends(oauth2_scheme)
):
    model_plane = session.get(ModelPlane, model_plane_id)
    if not model_plane:
        raise HTTPException(status_code=404, detail="Modèle d'avion non trouvé.")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(model_plane, key, value)

    session.add(model_plane)
    session.commit()
    session.refresh(model_plane)
    return model_plane

@router.delete("/model_plane/{model_plane_id}", tags=["Modèles d'avion"])
def delete_model_plane(
        model_plane_id: int,
        session: Session = Depends(db.get_session),
        token: str = Depends(oauth2_scheme)
):
    model_plane = session.get(ModelPlane, model_plane_id)
    if not model_plane:
        raise HTTPException(status_code=404, detail="Modèle d'avion non trouvé.")

    session.delete(model_plane)
    session.commit()
    return {"message": "Modèle d'avion supprimé avec succès."}
