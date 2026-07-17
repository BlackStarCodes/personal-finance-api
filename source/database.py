from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from source.config import URL


class Base(DeclarativeBase):
    pass


engine = create_engine(URL)


def get_session():
    with Session(engine) as session:
        yield session