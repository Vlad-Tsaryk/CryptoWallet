from typing import Any, Dict, Optional

from fastapi_mail import ConnectionConfig
from libcloud.storage.drivers.local import LocalStorageDriver
from pydantic import BaseSettings, SecretStr, validator, EmailStr
from sqlalchemy_file.storage import StorageManager


class Settings(BaseSettings):
    PROJECT_NAME: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_URI: str | None = None

    @validator("POSTGRES_URI", pre=True)
    def validate_postgres_conn(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        password: SecretStr = values.get("POSTGRES_PASSWORD", SecretStr(""))
        return "{scheme}://{user}:{password}@{host}/{db}".format(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=password.get_secret_value(),
            host=values.get("POSTGRES_HOST"),
            db=values.get("POSTGRES_DB"),
        )

    RABBITMQ_URL: str

    SECRET_KEY: SecretStr
    JWT_ALGORITHM: str

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
email_conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

# Configure Storage
# os.makedirs("/media/attachment", 0o777, exist_ok=True)
container = LocalStorageDriver("media").get_container("attachment")
StorageManager.add_storage("default", container)
