from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = "sqlite:///artefacts/hanoi.db"

# connect_args={"check_same_thread": False} is required for SQLite threads
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Declarative Base class for SQLAlchemy models."""

    pass


def get_db() -> Generator[Session, None, None]:
    """Dependency generator to get a thread-safe database session.

    Yields:
        A SQLAlchemy Session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
