import streamlit as st
from pathlib import Path
from core.models import JobPosting, JobSummary, InterviewNotes, JobStatus
from core.repositories import (
    JobPostingRepo,
    JobSummaryRepo,
    CompanyInfoRepo,
    ApplicationMaterialsRepo,
    InterviewNotesRepo,
)
from core.db import get_session
from core.utils import disappearing_message
from components.editable_interview_notes import render_editable_interview_notes

db_session = get_session()
jobs_repo = JobPostingRepo(db_session)
summary_repo = JobSummaryRepo(db_session)
company_info_repo = CompanyInfoRepo(db_session)
app_materials_repo = ApplicationMaterialsRepo(db_session)
interview_notes_repo = InterviewNotesRepo(db_session)

job_post = jobs_repo.get_by_id(4)
job_summary = summary_repo.get_by_job_post_id(4)
company_info = company_info_repo.get_by_id(4)
app_materials = app_materials_repo.get_by_job_post_id(4)
company_info = (
    company_info_repo.get_by_id(job_post.company_info_id)
    if job_post and job_post.company_info_id
    else None
)
past_interview_notes = interview_notes_repo.get_by_job_post_id(4)


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
    with st.form(
        key="update_status_form",
        clear_on_submit=False,
        enter_to_submit=True,
    ):
        current_status_index = 0
        if job_post and job_post.status:
            status_options = [status_option.display_name for status_option in JobStatus]
            try:
                current_status_index = status_options.index(
                    job_post.status.display_name
                )
            except ValueError:
                current_status_index = 0
        job_status = st.selectbox(
            label="status",
            options=status_options,
            index=current_status_index,
        )
        submit_btn = st.form_submit_button("update status")
        if submit_btn:
            try:
                new_status = JobStatus(job_status.replace(" ", "_").upper())
                new_job_status = jobs_repo.update(job_id=job_post.id, status=new_status)  # type: ignore[call-arg]
                disappearing_message(
                    st,
                    message="Status updated.",
                    msg_type="success",
                    duration=1,
                )
            except Exception as e:
                disappearing_message(
                    st, message="Error updating status.", msg_type="error", duration=3
                )


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
    # todo - add pdf download button
    # todo - make content editable + auto-save
    # todo - implement version history
    # todo - implement tailoring chat modal
    st.header("resume")
    st.markdown(f"{app_materials.resume if app_materials else '<Resume Content>'}")
    st.header("cover letter")
    st.markdown(
        f"{app_materials.cover_letter if app_materials else '<Cover Letter Content>'}"
    )

with interviewing:
    interview_notes, prep_materials, application_materials = st.tabs(
        ["Interview Notes", "Prep Materials", "Application Materials"]
    )
    with interview_notes:
        with st.form(
            key="interview_notes_form",
            clear_on_submit=True,
            enter_to_submit=True,
            border=True,
            width="stretch",
            height="content",
        ):
            st.text_input(
                label="Interview Notes Title (optional)",
                placeholder="e.g. Phone Screen with Jane Doe - Aug 15, 2023",
                key="interview_notes_title",
            )
            st.text_area(
                label="Add your interview notes here (markdown okay)...",
                placeholder="e.g. questions asked, your answers, feedback received, etc.",
                key="interview_notes_content",
            )
            submit_btn = st.form_submit_button("Save Notes")
            if submit_btn:
                # todo -- save notes to db
                interview_notes_repo.add(
                    InterviewNotes(
                        title=st.session_state.get("interview_notes_title", ""),
                        content=st.session_state.get("interview_notes_content", ""),
                        job_posting_id=job_post.id if job_post else None,
                    )
                )
                st.rerun()
                disappearing_message(
                    st,
                    message="Interview notes saved successfully!",
                    msg_type="success",
                    duration=2,
                )
        st.markdown("#### Past interviews:")
        if not interview_notes:
            st.info("No interview notes found. Add some using the form above!")
        else:
            for notes in past_interview_notes:
                render_editable_interview_notes(interview_notes=notes)
    with prep_materials:
        st.write(
            "future -- interview prep materials, e.g. coding challenges, behavioral questions, etc."
        )
    with application_materials:
        # ? how to link to version history once it's implemented? need a mechanism to select from version history when changing status to 'applied'
        st.header("Resume")
        st.markdown(f"{app_materials.resume if app_materials else '<Resume Content>'}")
        st.header("Cover Letter")
        st.markdown(
            f"{app_materials.cover_letter if app_materials else '<Cover Letter Content>'}"
        )
