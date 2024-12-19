from typing import Generator

from sqlalchemy import Column, DateTime, Integer, create_engine, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Session, declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///./exchange_rate.db'

# Create engine and session
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class BaseModel:
    '''
    This class will not create table itself
    All other models would inherit from this class
    '''

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


# Create a declarative base that will use the BaseModel
Base = declarative_base(cls=BaseModel)


def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
