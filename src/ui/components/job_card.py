import streamlit as st
from core.models import JobPosting
from utils import truncate


def render_job_card(job: JobPosting) -> None:
    with st.container():
        # Header row: title + basic info
        header_cols = st.columns([3, 2])
        with header_cols[0]:
            st.markdown(f"### {job.title}")
            st.markdown(f"**{job.company}** · {job.location}")
        with header_cols[1]:
            # Tags / meta info
            tags = []
            if job.job_type:
                tags.append(job.job_type)
            if job.experience_level:
                tags.append(job.experience_level)
            if job.source:
                tags.append(f"Source: {job.source}")
            if job.salary_range:
                tags.append(f"Salary: {job.salary_range}")

            if tags:
                st.markdown(" | ".join(f"`{t}`" for t in tags))

            if job.posted_date:
                st.caption(f"Posted: {job.posted_date}")
                #   .strftime('%Y-%m-%d')}")

        if job.summary:
            st.markdown("**About the job**")
            st.markdown(job.summary)

        # Actions
        action_cols = st.columns([1, 2])
        with action_cols[0]:
            if st.button("View details", key=f"details_{job.id}"):
                st.session_state[f"show_{job.id}"] = True

        with action_cols[1]:
            if job.url:
                st.link_button("Open original posting", job.url)

        # Full details in an expander
        with st.expander("Full job description", expanded=False):
            st.write(job.description)

        st.divider()
