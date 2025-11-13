from typing import Sequence
from sqlmodel import Session, select
from .db_models import JobSearchQuery, JobPosting


class JobSearchQueryRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> JobSearchQuery | None:
        return self.session.exec(
            select(JobSearchQuery).where(JobSearchQuery.id == id)
        ).first()

    def add(self, job_search_query: JobSearchQuery) -> JobSearchQuery:
        self.session.add(job_search_query)
        self.session.commit()
        self.session.refresh(job_search_query)
        return job_search_query


class JobPostingRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_by_url(self, url: str) -> JobPosting | None:
        return self.session.exec(
            select(JobPosting).where(JobPosting.url == url)
        ).first()

    def add(self, job_posting: JobPosting) -> JobPosting:
        self.session.add(job_posting)
        self.session.commit()
        self.session.refresh(job_posting)
        return job_posting

    def get_new(self) -> Sequence[JobPosting]:
        # e.g., jobs without summary/status yet
        return self.session.exec(
            select(JobPosting).where(JobPosting.summary == None)
        ).all()

    def update_job(self, job_id: int, **fields) -> JobPosting:
        statement = select(JobPosting).where(JobPosting.id == job_id)
        results = self.session.exec(statement)
        job = results.one()
        if job is None:
            raise ValueError(f"no job (id: {job_id}) found")

        for key, value in fields.items():
            if hasattr(job, key):
                setattr(job, key, value)

        self.session.add(job)
        self.session.commit()
        self.session.refresh(job)
        return job
