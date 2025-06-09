from fastapi import Depends, FastAPI, HTTPException
from database.connection import db
from sqlalchemy import text
from sqlmodel import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

# Importer les routeurs
from auth.auth import router as auth_router
from airport.airport import router as airport_router
from ModelPlane.model_plane import router as model_plane_router
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(airport_router)
app.include_router(model_plane_router)

# Appliquer le schéma OpenAPI personnalisé
app.openapi = lambda: custom_openapi(app)

@app.get("/")
def read_root():
    return {"message": "API OK"}

@app.get("/db/table", tags=["Utilitaires"])
def read_root(session: Session = Depends(db.get_session)):
    query = text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    result = session.exec(query).fetchall()

    tables = [row[0] for row in result]

    return {
        "message": "Voici les tables dans flyver_db",
        "tables": tables
    }


@app.get("/tables/{table_name}", tags=["Utilitaires"])
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

def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FLYVER API",
        version="1.0.0",
        description="Documentation de l'API avec support Bearer Token",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema