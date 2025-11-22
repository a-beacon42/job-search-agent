import streamlit as st
from core.models import JobPosting, JobSummary


def card(job_post: JobPosting, job_summary: JobSummary):
    st.markdown(
        f"""
        <div class="card">
            <h5>{job_post.title}</h5>
        </div>
    """,
        unsafe_allow_html=True,
    )
