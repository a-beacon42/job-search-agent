import streamlit as st
import datetime as dt
from sqlalchemy import func
from core.utils import disappearing_message
from core.models import ApplicantInfo
from core.repositories import ApplicantInfoRepo
from core.db import get_session

db = get_session()
app_info_repo = ApplicantInfoRepo(db)


@st.fragment
def render_editable_applicant_info(app_info: ApplicantInfo):
    app_info_to_display = app_info
    formatted_date = (
        app_info_to_display.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(app_info_to_display.updated_at, dt.datetime)
        else str(app_info_to_display.updated_at)
    )
    with st.expander(label=f"{app_info_to_display.title}", expanded=False):
        new_title = st.text_input(
            label=f"update title",
            #   (updated on: {formatted_date})",
            label_visibility="hidden",
            value=app_info_to_display.title or "",
            key=f"app_info_{app_info_to_display.id}_title",
        )
        new_content = st.text_area(
            label=f"update content",
            label_visibility="hidden",
            value=app_info_to_display.content,
            key=f"app_info_{app_info_to_display.id}_content",
            height=150,
        )
        if st.button("Save Changes", key=f"save_app_info_{app_info_to_display.id}"):
            try:
                app_info_repo.update(app_info_to_display.id, title=new_title, content=new_content)  # type: ignore[arg-type]
                st.toast("Applicant info updated successfully!")
                st.rerun()
            except Exception as e:
                disappearing_message(
                    st=st,
                    message="Error updating applicant info",
                    msg_type="error",
                    duration=3,
                )
                st.error(f"Error updating applicant info: {str(e)}")
        if st.button("Delete", key=f"delete_app_info_{app_info_to_display.id}"):  # type: ignore[call-arg]
            try:
                app_info_repo.delete(app_info_to_display.id)  # type: ignore[arg-type]
                st.toast("Applicant info deleted successfully!")
                st.rerun()
            except Exception as e:
                disappearing_message(
                    st=st,
                    message="Error deleting applicant info",
                    msg_type="error",
                    duration=3,
                )
