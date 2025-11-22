from datetime import datetime
from typing import Optional
from enum import Enum

from sqlmodel import SQLModel, Field


class JobType(str, Enum):
    FULL_TIME = "FULL_TIME"
    CONTRACT_TO_HIRE = "CONTRACT_TO_HIRE"
    CONTRACT = "CONTRACT"
    NOT_LISTED = "NOT_LISTED"

    @property
    def display_name(self) -> str:
        return {
            "FULL_TIME": "Full Time",
            "CONTRACT_TO_HIRE": "Contract to Hire",
            "CONTRACT": "Contract",
            "NOT_LISTED": "Not Listed",
        }.get(self.value, self.value)


class ExperienceLevel(str, Enum):
    ENTRY_LEVEL = "ENTRY_LEVEL"
    MID_LEVEL = "MID_LEVEL"
    SR_LEVEL = "SR_LEVEL"
    NOT_LISTED = "NOT_LISTED"

    @property
    def display_name(self) -> str:
        return {
            "ENTRY_LEVEL": "Entry Level",
            "MID_LEVEL": "Mid Level",
            "SR_LEVEL": "Senior Level",
            "NOT_LISTED": "Not Listed",
        }.get(self.value, self.value)


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

    created_at: datetime = Field(default_factory=datetime.utcnow)

    search_query_id: Optional[int] = Field(
        default=None,
        foreign_key="jobsearchquery.id",
    )
    job_summary_id: Optional[int] = Field(default=None, foreign_key="jobsummary.id")


class JobDetails(SQLModel):
    standout_features: str = Field(
        description="""highlight main details about the job - focus on unique aspects & less on common things
                    - role & responsibilities 
                    - company mission & culture 
                    - PTO & benefits
                    """
    )
    qualifications: str = Field(
        description="""main qualifications highlighted in the job description
                    - tech stack
                    - skills
                    - education
                    - nice to haves
                    """
    )


class JobSummary(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    salary_range: str = Field(
        description="salary range for the posted role, i.e. '$150k-175k' or 'not listed'"
    )
    job_type: JobType
    experience_level: ExperienceLevel

    standout_features: str = Field(
        description="""highlight main details about the job - focus on unique aspects & less on common things
                    - role & responsibilities 
                    - company mission & culture 
                    - PTO & benefits
                    """
    )
    qualifications: str = Field(
        description="""main qualifications highlighted in the job description
                    - tech stack
                    - skills
                    - education
                    - nice to haves
                    """
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)
    job_posting_id: Optional[int] = Field(default=None, foreign_key="jobposting.id")
