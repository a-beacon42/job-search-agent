import streamlit as st
from core.db import get_session
from core.repositories import JobPostingRepo, JobSummaryRepo
from ui.components.job_card import render_job_card

# todo - add selector for job cards & bulk apply action (make apply async first)
NUM_COLS = 3


db_session = get_session()
jobs_repo = JobPostingRepo(db_session)
summaries_repo = JobSummaryRepo(db_session)

st.set_page_config(page_title="Job Search Assistant", layout="wide")

st.title("Job Search Assistant")
with st.sidebar:
    st.header("filters")
    query = st.text_input("Search jobs", placeholder="Titles, company, keywords...")

    locations = jobs_repo.get_locations()
    location_filter = st.selectbox(
        "Location",
        options=["All", locations],
        index=0,
    )

    sort_by = st.selectbox(
        "Sort by",
        options=["Recently posted", "Company A → Z"],
    )

jobs = jobs_repo.search_jobs(query=query, location=location_filter, sort_by=sort_by)  # type: ignore[return-value]

st.subheader(f"{len(jobs)} job(s) found")

if not jobs:
    st.info("No jobs match your filters yet. Try broadening your search.")

else:
    for row_start in range(0, len(jobs), NUM_COLS):
        row_jobs = jobs[row_start : row_start + NUM_COLS]
        cols = st.columns(len(row_jobs))

        for col, job in zip(cols, row_jobs):
            summary = summaries_repo.get_by_job_post_id(job.id)  # type: ignore[return-value]
            with col:
                with st.container(border=True, height="stretch"):
                    render_job_card(job, summary)  # type: ignore[return-value]
