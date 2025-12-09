import streamlit as st
from pathlib import Path
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
        st.title(f"welcome, {user.first_name}")

        home_tabs = [
            "App Status",
            "Applicant Info",
        ]

        col_names = ["New Jobs", "Ready to Apply", "Applied"]
        cols = st.columns(len(col_names))

        for col, name in zip(cols, col_names):
            with col:
                st.metric(label=name, value="42")  # placeholder value

    else:
        st.write(f"no logged in user found")

except Exception as e:
    st.error(f"no user: {str(e)}")
    st.switch_page(page="/pages/login_register.py")

st.markdown("under construction -- future home will look something like:")
st.markdown(
    """
- simple dashboard  
- **top row of quick check metrics**: 
    * number of new jobs to review, [clicking takes to new jobs] 
    * number of jobs read to apply to, 
    * breakdown of status of applied to jobs (applied, 1st round, late stage, rejected, stale (need to define 'stale'))  
- **table to show more detail**:  
    * 1 row per job post  
    * filters for status  
    * clicking on single job will route to job detail page  
"""
)
