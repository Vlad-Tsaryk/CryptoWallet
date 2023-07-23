from pydantic import BaseSettings


class Settings(BaseSettings):
    INFRA_WSS_URL: str
    RABBITMQ_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
