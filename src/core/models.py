from datetime import datetime
from typing import Optional
from enum import Enum

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

    created_at: datetime = Field(default_factory=datetime.utcnow)

    search_query_id: Optional[int] = Field(
        default=None,
        foreign_key="jobsearchquery.id",
    )
    job_summary_id: Optional[int] = Field(default=None, foreign_key="jobsummary.id")
    company_info_id: Optional[int] = Field(default=None, foreign_key="companyinfo.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


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


class ApplicantInfoType(str, Enum):
    PAST_EXPERIENCE = "PAST_EXPERIENCE"
    TECHNICAL_SKILL = "TECHNICAL_SKILL"
    PROJECT = "PROJECT"
    EDUCATION = "EDUCATION"

    @property
    def display_name(self) -> str:
        return {
            "PAST_EXPERIENCE": "Past Experience",
            "TECHNICAL_SKILL": "Technical Skill",
            "PROJECT": "Project",
            "EDUCATION": "Education",
        }.get(self.value, self.value)


class ApplicantInfo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    info_type: ApplicantInfoType = Field(
        description="""type of information, e.g. past experience, technical skill, project, education"""
    )
    content: str = Field(
        description="""content of the information, e.g. description of past experience, technical skill, project, education"""
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class ApplicationMaterials(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cover_letter: str = Field(
        description="""cover letter tailored to match job description with applicant's background & skills"""
    )
    resume: str = Field(
        description="""resume tailored to match job description with applicant's background & skills"""
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    job_posting_id: Optional[int] = Field(default=None, foreign_key="jobposting.id")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(description="""user's first name""")
    last_name: str = Field(description="""user's last name""")
    email: str = Field(description="""user's email""")
    password_hash: str = Field(description="""hashed user password""")
    is_active: bool = Field(default=True, description="""active user account""")
    email_verified: bool = Field(
        default=False, description="""user has verified account from email"""
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CompanyInfo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(description="""company name""")
    overview: str = Field(
        description="""brief overview of the company, what it does, industry"""
    )
    products_services: str = Field(
        description="""description of key products, services, customers, and market segment"""
    )
    size_locations: str = Field(
        description="""description of company size (employees, revenue range if available) and main offices/regions"""
    )
    culture: str = Field(
        description="""description of company culture, values, work environment"""
    )
    recent_news: str = Field(
        description="""recent news about the company, e.g. product launches, funding, leadership changes"""
    )
    appeal_to_applicants: str = Field(
        description="""aspects of the company that might appeal to job applicants"""
    )
    potential_concerns: str = Field(
        description="""any potential concerns or red flags for job applicants"""
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
