from sqlmodel import Session, SQLModel, create_engine

from . import config

settings = config.Settings()
engine = create_engine(settings.dsn(), echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)
