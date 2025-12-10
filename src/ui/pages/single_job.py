import streamlit as st
from pathlib import Path
from core.models import JobPosting, JobSummary
from core.repositories import (
    JobPostingRepo,
    JobSummaryRepo,
    CompanyInfoRepo,
    ApplicationMaterialsRepo,
)
from core.db import get_session

db_session = get_session()
jobs_repo = JobPostingRepo(db_session)
summary_repo = JobSummaryRepo(db_session)
company_info_repo = CompanyInfoRepo(db_session)
app_materials_repo = ApplicationMaterialsRepo(db_session)

job_post = jobs_repo.get_by_id(4)
job_summary = summary_repo.get_by_job_post_id(4)
company_info = company_info_repo.get_by_id(4)
app_materials = app_materials_repo.get_by_job_post_id(4)
company_info = (
    company_info_repo.get_by_id(job_post.company_info_id)
    if job_post and job_post.company_info_id
    else None
)


with st.sidebar:
    st.header("filters")
    query = st.text_input("Search jobs", placeholder="Titles, company, keywords...")

    locations = jobs_repo.get_locations()
    location_filter = st.selectbox(
        "Location",
        options=["All"] + locations,  # type: ignore[arg-type]
        index=0,
    )

    sort_by = st.selectbox(
        "Sort by",
        options=["Recently posted", "Company A → Z"],
    )

header_cols = st.columns([3, 1], vertical_alignment="center")
with header_cols[0]:
    st.title(f":green[{job_post.title if job_post else '<Job Title>'}]")
with header_cols[1]:
    st.markdown("`status: new`")

company_name, location, salary_range, posted_date = st.columns(
    4, vertical_alignment="bottom"
)
with company_name:
    st.markdown(f"#### :green[{job_post.company if job_post else '<Company Name>'}]")
with location:
    st.markdown(f":green[location]: {job_post.location if job_post else '<Location>'}")
with salary_range:
    st.markdown(
        f":green[salary]: {job_post.salary_range if job_post else '<Salary Range>'}"
    )
with posted_date:
    st.markdown(
        f":green[posted]: {job_post.created_at.strftime('%b %d, %Y') if job_post and job_post.created_at else '<Posted Date>'}"
    )

(
    job_description,
    company_summary,
    application,
    interviewing,
    negotiation_prep,
    close_out_notes,
) = st.tabs(
    [
        "Job Description",
        "Company Info",
        "Application",
        "Interviewing",
        "Negotiation Prep",
        "Close Out Notes",
    ]
)

with job_description:
    st.header("job summary")
    if job_summary and job_summary.standout_features:
        st.markdown(f"{job_summary.standout_features}")
    if job_summary and job_summary.qualifications:
        st.markdown(f"{job_summary.qualifications}")
    else:
        st.markdown("No job summary available.")

    st.header("full post")
    if job_summary and job_post and job_post.description:
        st.html(f"{job_post.description}")
    else:
        st.markdown("No job description available.")

with company_summary:
    if not company_info:
        st.markdown("No company info available.")
    else:
        st.markdown("#### company overview")
        st.markdown(f"{company_info.overview}")

        st.markdown("#### recent news & notable events")
        st.markdown(f"{company_info.recent_news}")

        st.markdown("#### culture & work environment")
        st.markdown(f"{company_info.culture}")

        st.markdown("#### size & locations")
        st.markdown(f"{company_info.size_locations}")

        st.markdown("#### products / services & market")
        st.markdown(f"{company_info.products_services}")

        st.markdown("#### why it might appeal to an applicant")
        st.markdown(f"{company_info.appeal_to_applicants}")

        st.markdown("#### potential concerns / things to research further")
        st.markdown(f"{company_info.potential_concerns}")

with application:
    st.header("resume")
    st.markdown(f"{app_materials.resume if app_materials else '<Resume Content>'}")
    st.header("cover letter")
    st.markdown(
        f"{app_materials.cover_letter if app_materials else '<Cover Letter Content>'}"
    )

with interviewing:
    st.markdown(
        """
resume & cover letter  
* download button
* editable
* ?auto-save
* version history
* chat modal for tailoring to job description
                """
    )
    interview_notes, prep_materials, application_materials = st.tabs(
        ["Interview Notes", "Prep Materials", "Application Materials"]
    )
    with interview_notes:
        st.write("future -- interview notes, questions asked, etc.")
    with prep_materials:
        st.write(
            "future -- interview prep materials, e.g. coding challenges, behavioral questions, etc."
        )
    with application_materials:
        st.header("Resume")
        st.markdown(f"{app_materials.resume if app_materials else '<Resume Content>'}")
        st.header("Cover Letter")
        st.markdown(
            f"{app_materials.cover_letter if app_materials else '<Cover Letter Content>'}"
        )
