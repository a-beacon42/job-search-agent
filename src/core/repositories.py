from typing import Sequence, List, Optional
from sqlmodel import Session, select
from sqlalchemy import func, desc
from .models import (
    JobSearchQuery,
    JobPosting,
    JobSummary,
    ApplicantInfo,
    ApplicationMaterials,
    User,
    CompanyInfo,
)


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

    def get_all(self) -> Sequence[JobPosting]:
        return self.session.exec(select(JobPosting)).all()

    def get_by_url(self, url: str) -> JobPosting | None:
        return self.session.exec(
            select(JobPosting).where(JobPosting.url == url)
        ).first()

    def get_by_id(self, id: int) -> JobPosting | None:
        return self.session.exec(select(JobPosting).where(JobPosting.id == id)).first()

    def get_by_user_id(self, user_id: int) -> List[JobPosting] | None:
        statement = select(JobPosting).where(user_id == user_id)
        job_posts = self.session.exec(statement).all()
        return job_posts  # type: ignore[return-value]

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

    def get_locations(self) -> Sequence[str]:
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


class ApplicantInfoRepo:
    def __init__(self, session) -> None:
        self.session = session

    def get_info_by_user_id(self, user_id: int) -> Sequence[ApplicantInfo]:
        statement = select(ApplicantInfo).where(user_id == user_id)
        results = self.session.exec(statement).all()
        return results

    def add(self, app_info: ApplicantInfo) -> ApplicantInfo:
        self.session.add(app_info)
        self.session.commit()
        self.session.refresh(app_info)
        return app_info

    def update(self, app_info_id: int, **fields) -> ApplicantInfo:
        statement = select(ApplicantInfo).where(ApplicantInfo.id == app_info_id)
        app_info = self.session.exec(statement).one()
        if app_info is None:
            raise ValueError(f"ApplicantInfo (id: {app_info_id}) not found")

        for key, value in fields.items():
            if hasattr(app_info, key):
                setattr(app_info, key, value)

        self.session.add(app_info)
        self.session.commit()
        self.session.refresh(app_info)
        return app_info

    def delete(self, app_info_id: int) -> None:
        statement = self.session.select(ApplicantInfo).where(id=app_info_id)
        app_info = self.session.exec(statement).one()
        self.session.delete(app_info)
        self.session.commit()


class ApplicationMaterialsRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> Sequence[ApplicationMaterials]:
        return self.session.exec(select(ApplicationMaterials)).all()

    def get_by_id(self, id: int) -> ApplicationMaterials | None:
        return self.session.exec(
            select(ApplicationMaterials).where(ApplicationMaterials.id == id)
        ).first()

    def get_by_job_post_id(self, job_post_id: int) -> ApplicationMaterials | None:
        return self.session.exec(
            select(ApplicationMaterials).where(
                ApplicationMaterials.job_posting_id == job_post_id
            )
        ).first()

    def add(self, app_materials: ApplicationMaterials) -> ApplicationMaterials:
        self.session.add(app_materials)
        self.session.commit()
        self.session.refresh(app_materials)
        return app_materials


class UserRepo:
    def __init__(self, session: Session):
        self.session = session

    def register_user(self, new_user: User) -> User:
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def get_by_id(self, id: int) -> User | None:
        statement = select(User).where(User.id == id)
        results = self.session.exec(statement=statement)
        user = results.first()
        return user

    def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        results = self.session.exec(statement=statement)
        user = results.first()
        return user

    def update_user(self, user_id: int, **fields) -> User:
        statement = select(User).where(User.id == user_id)
        results = self.session.exec(statement)
        user = results.one()
        if user is None:
            raise ValueError(f"no user (id: {user_id}) found")
        for k, v in fields.items():
            if hasattr(user, k):
                setattr(user, k, v)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user


class CompanyInfoRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> CompanyInfo | None:
        return self.session.exec(
            select(CompanyInfo).where(CompanyInfo.id == id)
        ).first()

    def get_by_name(self, name: str = "") -> CompanyInfo | None:
        like_pattern = f"%{name.lower()}%"
        return self.session.exec(
            select(CompanyInfo).where(func.lower(CompanyInfo.name).like(like_pattern))
        ).first()

    def add(self, company_info: CompanyInfo) -> CompanyInfo:
        self.session.add(company_info)
        self.session.commit()
        self.session.refresh(company_info)
        return company_info
