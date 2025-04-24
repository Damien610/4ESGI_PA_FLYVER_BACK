from fastapi import Depends, FastAPI, HTTPException
from database.connection import db
from sqlalchemy import text
from sqlmodel import Session

from auth.auth import router as auth_router

app = FastAPI()
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "API OK"}

@app.get("/db/table")
def read_root(session: Session = Depends(db.get_session)):
    query = text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    result = session.exec(query).fetchall()

    tables = [row[0] for row in result]

    return {
        "message": "Voici les tables dans flyver_db",
        "tables": tables
    }


@app.get("/tables/{table_name}")
def list_table_data(table_name: str, session: Session = Depends(db.get_session)):
    try:
        result = session.exec(text(f"SELECT * FROM {table_name}")).fetchall()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de l'accès à la table '{table_name}': {str(e)}")

    if not result:
        return {"message": f"La table '{table_name}' est vide ou n'existe pas."}

    # On convertit les lignes en dicts (si possible)
    data = [dict(row._mapping) for row in result]

    return {
        "table": table_name,
        "rows": data
    }