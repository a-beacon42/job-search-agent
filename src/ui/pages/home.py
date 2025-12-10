import time
from typing import cast
import streamlit as st
from core.utils import group_by, disappearing_message
from core.models import ApplicantInfoType, ApplicantInfo
from core.repositories import UserRepo, JobPostingRepo, ApplicantInfoRepo
from core.db import get_session


st.set_page_config(page_title="Home", page_icon=":house:", layout="wide")

db = get_session()
user_repo = UserRepo(db)
job_posting_repo = JobPostingRepo(db)
appl_info_repo = ApplicantInfoRepo(db)

try:
    user_id = st.session_state.get("user_id")
    if isinstance(user_id, list):
        user_id = user_id[0]

    try:
        user = user_repo.get_by_id(int(user_id))  # type: ignore[return-value]
        user_jobs = job_posting_repo.get_by_user_id(int(user_id))  # type: ignore[return-value]
        user_app_info = appl_info_repo.get_info_by_user_id(int(user_id))  # type: ignore[return-value]
    except Exception as e:
        st.error(f"Error loading logged in user: {str(e)}")
        st.switch_page(page="/pages/login_register.py")

    if user:
        st.title(f":green[Welcome, {user.first_name}]")

        app_status, applicant_info = st.tabs(
            [
                "App Status",
                "Applicant Info",
            ]
        )

        with app_status:
            col_names = ["New Jobs", "Ready to Apply", "Applied"]
            cols = st.columns(len(col_names))

            for col, name in zip(cols, col_names):
                with col:
                    st.metric(label=name, value="42")  # placeholder value

        with applicant_info:
            st.markdown("##### add something new:")
            with st.form(
                key="add_app_info_form",
                clear_on_submit=True,
                enter_to_submit=True,
                border=True,
                width="stretch",
                height="content",
            ):
                info, info_type = st.columns([3, 1])
                with info:
                    st.text_area(
                        label="Share something about your background",
                        placeholder="e.g. 5 years experience in software engineering...",
                        key="app_info_content",
                    )
                with info_type:
                    option = st.selectbox(
                        "What kind of info are you adding?",
                        [info_type.display_name for info_type in ApplicantInfoType],
                    )
                    submit_btn = st.form_submit_button("Add Info")
                if submit_btn:
                    # todo -- add validation, error handling
                    selected_type = ApplicantInfoType(
                        option.replace(" ", "_").upper()
                    )  # todo -- this is ugly; learn more about enums
                    new_app_info = appl_info_repo.add(
                        ApplicantInfo(
                            info_type=selected_type,
                            content=st.session_state.get("app_info_content", ""),
                            user_id=user.id,
                        )
                    )
                    disappearing_message(
                        st,
                        message="Applicant info added successfully!",
                        msg_type=cast(type[str], "success"),
                        duration=2,
                    )  # type: ignore[call-arg]

            st.subheader("about you:")
            if len(user_app_info) <= 0:
                st.info("No applicant info found. Add some using the form above!")
            else:
                grouped_app_info = group_by(user_app_info, "info_type")
                for type, infos in grouped_app_info.items():
                    st.markdown(f"##### {type.display_name}")
                    for info in infos:
                        st.markdown(f"* {info.content}")
                # for info in user_app_info or []:
                #     # todo -- group by type, make collapsible sections
                #     st.markdown(f"**{info.info_type.display_name}**")
                #     st.write(info.content)
                #     st.markdown("---")

    else:
        st.write(f"no logged in user found")

except Exception as e:
    st.error(f"unknown error: {str(e)}")
    disappearing_message(
        st=st,
        message="Unexpected error occurred. Please log in again.",
        msg_type=cast(type[str], "error"),  # type: ignore[call-arg]
        duration=5,
    )

# - simple dashboard
# - **top row of quick check metrics**:
#     * number of new jobs to review, [clicking takes to new jobs]
#     * number of jobs read to apply to,
#     * breakdown of status of applied to jobs (applied, 1st round, late stage, rejected, stale (need to define 'stale'))
# - **table to show more detail**:
#     * 1 row per job post
#     * filters for status
#     * clicking on single job will route to job detail page
# """
# )
