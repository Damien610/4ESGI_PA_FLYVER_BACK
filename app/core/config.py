from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    environment: str
    database_url: str
    secret_key: str

    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    db_driver: str

    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str
    model_config = SettingsConfigDict(env_file=".env")

    @property
    def full_db_url(self) -> str:
        return "mssql+pyodbc://sa:YourStrong%40Password123@sqlserver:1433/flyver_db?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no"

settings = Settings()
