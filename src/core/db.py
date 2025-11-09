from sqlmodel import SQLModel, create_engine, Session

from .db_models import (
    JobSearchQuery,
    JobPosting,
)

DATABASE_URL = "sqlite:///./job_search.db"

engine = create_engine(
    DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)


def init_db() -> None:
    """Create all tables in the database if they don't exist"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Get a new SQLModel Session."""
    return Session(engine)
