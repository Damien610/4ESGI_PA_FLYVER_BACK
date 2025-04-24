from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
from .models import User

class Database:
    def __init__(self):
        self.base_url = "mssql+pyodbc://sa:YourStrong%40Password123@sqlserver,1433"
        self.database_name = "flyver_db"
        self.full_url = f"{self.base_url}/{self.database_name}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no"
        self.engine = self._init_database()

    def _init_database(self):
        from sqlalchemy import text  # Ajout utile ici

        master_url = f"{self.base_url}/master?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no"
        master_engine = create_engine(master_url, echo=True)

        # Autocommit obligatoire pour CREATE DATABASE
        with master_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            result = conn.execute(
                text(f"SELECT name FROM sys.databases WHERE name = '{self.database_name}'")
            )
            exists = result.fetchone()
            if not exists:
                conn.execute(text(f"CREATE DATABASE {self.database_name}"))
                print(f"✅ Base de données '{self.database_name}' créée.")

        db_engine = create_engine(self.full_url, echo=True)

        SQLModel.metadata.create_all(db_engine)
        print("✅ Tables vérifiées / créées.")

        return db_engine


    def get_session(self) -> Generator[Session, None, None]:
        with Session(self.engine) as session:
            yield session

db = Database()
