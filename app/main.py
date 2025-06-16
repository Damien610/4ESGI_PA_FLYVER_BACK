from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlalchemy import text
from sqlmodel import Session
from app.core.database import db

# Importer les routeurs
from app.routers.auth import router as auth_router
from app.routers.user import router as user_router
from app.routers.passenger import router as passenger_router
from app.routers.airport import router as airport_router
from app.routers.modelplane import router as modelplane_router
app = FastAPI()

# === CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Inclusion des routeurs ===
app.include_router(auth_router, tags=["Authentification"])
app.include_router(user_router, tags=["Users"])
app.include_router(passenger_router, tags=["Passengers"])
app.include_router(airport_router, tags=["Airports"])
app.include_router(modelplane_router, tags=["Model Planes"])

@app.on_event("startup")
def on_startup():
    try:
        with next(db.get_session()) as session:
            session.exec(text("SELECT 1"))
        print("✅ Connexion à la base de données réussie.")
    except Exception as e:
        print("❌ Erreur lors de la connexion à la base de données :", str(e))


@app.on_event("shutdown")
def on_shutdown():
    print("👋 Arrêt de l'application.")

# === OpenAPI personnalisé ===
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

app.openapi = lambda: custom_openapi(app)

# === Routes utilitaires ===

@app.get("/")
def root_status():
    return {"message": "API OK"}

@app.get("/db/tables", tags=["Utilitaires"])
def list_tables(session: Session = Depends(db.get_session)):
    query = text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    result = session.exec(query).fetchall()
    tables = [row[0] for row in result]
    return {
        "message": "Voici les tables dans flyver_db",
        "tables": tables
    }

@app.get("/db/tables/{table_name}", tags=["Utilitaires"])
def list_table_data(table_name: str, session: Session = Depends(db.get_session)):
    try:
        result = session.exec(text(f"SELECT * FROM {table_name}")).fetchall()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de l'accès à la table '{table_name}': {str(e)}")

    if not result:
        return {"message": f"La table '{table_name}' est vide ou n'existe pas."}

    data = [dict(row._mapping) for row in result]
    return {
        "table": table_name,
        "rows": data
    }
