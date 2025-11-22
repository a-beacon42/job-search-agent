from typing import Sequence, List, Optional
from sqlmodel import Session, select
from sqlalchemy import func, desc
from .models import JobSearchQuery, JobPosting, JobSummary


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
            select(JobPosting).where(JobPosting.job_summary_id == None)
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

    def search_jobs(
        self,
        query: str = "",
        location: Optional[str] = None,
        sort_by: str = "Recently posted",
    ) -> Sequence[JobPosting]:
        stmt = select(JobPosting)

        # text search over title, company, description
        if query:
            like = f"%{query.lower()}%"
            stmt = stmt.where(
                func.lower(JobPosting.title).like(like)
                | func.lower(JobPosting.company).like(like)
                | func.lower(JobPosting.description).like(like)
            )

        if location and location != "All":
            stmt = stmt.where(JobPosting.location == location)

        if sort_by == "Recently posted":
            stmt = stmt.order_by(JobPosting.created_at.desc().nullslast())  # type: ignore[return-value]

        elif sort_by == "Company A → Z":
            stmt = stmt.order_by(JobPosting.company.asc(), JobPosting.title.asc())  # type: ignore[return-value]

        else:
            stmt = stmt.order_by(JobPosting.id.desc())  # type: ignore[return-value]

        jobs = self.session.exec(stmt).all()

        return jobs

    def get_locations(self) -> List[str]:
        """Return distinct locations for filter dropdown."""
        rows = self.session.exec(
            select(JobPosting.location).distinct().where(JobPosting.location != "")
        ).all()
        # rows is a list of one-tuples like [('Remote',), ('NYC',)]
        locations = sorted({r for r in rows if r is not None})
        return locations


class JobSummaryRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> JobSummary | None:
        return self.session.exec(select(JobSummary).where(JobSummary.id == id)).first()

    def get_by_job_post_id(self, job_post_id: int) -> JobSummary | None:
        return self.session.exec(
            select(JobSummary).where(JobSummary.job_posting_id == job_post_id)
        ).first()

    def add(self, job_summary: JobSummary) -> JobSummary:
        self.session.add(job_summary)
        self.session.commit()
        self.session.refresh(job_summary)
        return job_summary

    def update_job(self, summary_id: int, **fields) -> JobSummary:
        statement = select(JobSummary).where(JobSummary.id == summary_id)
        results = self.session.exec(statement)
        summary = results.one()
        if summary is None:
            raise ValueError(f"no summary (id: {summary_id}) found")

        for key, value in fields.items():
            if hasattr(summary, key):
                setattr(summary, key, value)

        self.session.add(summary)
        self.session.commit()
        self.session.refresh(summary)
        return summary
