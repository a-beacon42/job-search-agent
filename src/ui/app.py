import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from core.db import get_session
from core.repositories import JobPostingRepo
from ui.components.job_card import render_job_card


def main():
    db_session = get_session()
    jobs_repo = JobPostingRepo(db_session)

    st.set_page_config(page_title="Job Search Assistant", layout="wide")

    st.title("Job Search Assistant")

    with st.sidebar:
        st.header("filters")
        query = st.text_input("Search jobs", placeholder="Titles, company, keywords...")

    jobs = jobs_repo.search_jobs(
        query=query
    )  # , location=location_filter, sort_by=sort_by)

    st.subheader(f"{len(jobs)} job(s) found")

    if not jobs:
        st.info("No jobs match your filters yet. Try broadening your search.")
        return

    for job in jobs:
        render_job_card(job)


if __name__ == "__main__":
    main()
