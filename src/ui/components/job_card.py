import streamlit as st
from core.models import JobPosting, JobSummary
from services.apply.apply import create_job_app


def handle_create_app(job_post: str):

    job_app = create_job_app(job_post, applicant_info)
    print(
        f"""
==================================================

creating resume & cover letter for Job {job_post}

==================================================
"""
    )


# todo -- fix applicant_info
applicant_info = "Experienced software developer with a strong background in Python and web development."


def render_job_card(job_post: JobPosting, job_summary: JobSummary):
    with st.container():
        title, apply_bttn = st.columns(spec=[0.75, 0.25])

        title.markdown(f"#### {job_post.title}")
        apply_bttn.button(
            "apply",
            key=job_post.id,
            help="click here to create a resume & cover letter for this job",
            on_click=handle_create_app,
            kwargs={"job_post": job_post.description, "applicant_info": applicant_info},
        )

    st.markdown(f"**{job_post.company}** · {job_post.location}")

    tags = []
    if job_summary.job_type:
        tags.append(f"{job_summary.job_type.display_name}")
    if job_summary.salary_range:
        (
            tags.append(f"{job_summary.salary_range}")
            if job_summary.salary_range != "not listed"
            else tags.append("$n/a")
        )
    if job_summary.experience_level:
        tags.append(f"{job_summary.experience_level.display_name}")
    if job_post.source:

        tags.append(f"{job_post.source}")

    if tags:
        st.markdown(" | ".join(f"`{t}`" for t in tags))

    if job_post.posted_date:
        st.caption(job_post.posted_date)

    st.markdown("**standout features**")
    features = job_summary.standout_features.split("- ")
    cleaned_features = [f for f in features if len(f) > 0]

    for f in cleaned_features:
        st.markdown(f":small[• {f}]")

    st.markdown("**qualifications**")
    quals = job_summary.qualifications.split("- ")
    cleaned_quals = [q for q in quals if len(q) > 0]
    for q in cleaned_quals:
        st.markdown(f":small[• {q}]")

    if job_post.url:
        st.link_button("View posting", job_post.url)
