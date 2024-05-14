from pydantic_settings import BaseSettings

from . import database


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    class Config:
        case_sensitive = True
        env_file = ".env"

    def dsn(self):
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


def get_db():
    db = database.get_session()
    try:
        yield db
    finally:
        db.close()
