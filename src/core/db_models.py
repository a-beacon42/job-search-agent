from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class JobSearchQuery(SQLModel, table=True):
    """Table storing each search you ran."""

    id: Optional[int] = Field(default=None, primary_key=True)

    keywords: str
    location: str = "United States"
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    remote_ok: bool = True
    max_results: int = 20

    created_at: datetime = Field(default_factory=datetime.utcnow)


class JobPosting(SQLModel, table=True):
    """Table storing job postings discovered by the job_discovery service."""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    company: str
    location: str
    description: str
    url: str
    posted_date: Optional[str] = None  # keep as string for now, can normalize later
    source: str
    salary_range: Optional[str] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    summary: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Optional link back to the search that found this posting
    search_query_id: Optional[int] = Field(
        default=None,
        foreign_key="jobsearchquery.id",
    )
