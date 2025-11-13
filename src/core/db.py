from typing import List
from sqlmodel import SQLModel, create_engine, Session
import os

from .models import (
    JobSearchQuery,
    JobPosting,
)

# Use absolute path to ensure consistency
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_PATH = os.path.join(PROJECT_ROOT, "job_search.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)


def init_db() -> None:
    """Create all tables in the database if they don't exist"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Get a new SQLModel Session."""
    return Session(engine)
