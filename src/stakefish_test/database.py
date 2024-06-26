from sqlmodel import Session, SQLModel, create_engine

from . import config

settings = config.Settings()
engine = create_engine(settings.dsn())


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
