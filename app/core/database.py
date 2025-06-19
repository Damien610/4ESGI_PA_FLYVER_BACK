from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
from app.core.config import settings
from sqlalchemy import text

print(settings.full_db_url)
class Database:
    def __init__(self):
        self.master_url = "mssql+pyodbc://sa:YourStrong%40Password123@sqlserver:1433/master?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no"

        self.full_url = settings.full_db_url
        self.database_name = settings.db_name
        self.engine = self._init_database()

    def _init_database(self):
        try:
            master_engine = create_engine(self.master_url, echo=True)

            with master_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
                print(f"🔍 Vérification de l'existence de la base '{self.database_name}'...")
                result = conn.execute(
                    text("SELECT name FROM sys.databases WHERE name = :name"),
                    {"name": self.database_name}
                )
                if not result.fetchone():
                    print(f"🛠 Création de la base '{self.database_name}'...")
                    conn.execute(text(f"CREATE DATABASE [{self.database_name}]"))
                    print(f"✅ Base de données '{self.database_name}' créée.")
                else:
                    print(f"✅ Base '{self.database_name}' déjà existante.")

        except Exception as e:
            print(f"❌ Erreur pendant la création de la base : {e}")
            raise

        from app.models.user import User
        from app.models.passenger import Passenger
        from app.models.airport import Airport
        from app.models.plane import Plane
        from app.models.flight import Flight
        from app.models.reservation import Reservation
        from app.models.modelplane import ModelPlane
        db_engine = create_engine(self.full_url, echo=True)
        SQLModel.metadata.create_all(db_engine)
        print("✅ Tables vérifiées / créées.")
        return db_engine


    def get_session(self) -> Generator[Session, None, None]:
        with Session(self.engine) as session:
            yield session


db = Database()
