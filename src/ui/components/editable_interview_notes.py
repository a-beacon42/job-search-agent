import streamlit as st
import datetime as dt
from sqlalchemy import func
from core.utils import disappearing_message
from core.models import InterviewNotes
from core.repositories import InterviewNotesRepo
from core.db import get_session

db = get_session()
interview_notes_repo = InterviewNotesRepo(db)


@st.fragment
def render_editable_interview_notes(interview_notes: InterviewNotes):
    interview_notes_to_display = interview_notes
    formatted_date = (
        interview_notes_to_display.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(interview_notes_to_display.updated_at, dt.datetime)
        else str(interview_notes_to_display.updated_at)
    )
    with st.expander(label=f"{interview_notes_to_display.title}", expanded=False):
        new_title = st.text_input(
            label=f"update title",
            #   (updated on: {formatted_date})",
            label_visibility="hidden",
            value=interview_notes_to_display.title or "",
            key=f"interview_notes_{interview_notes_to_display.id}_title",
        )
        new_content = st.text_area(
            label=f"update content",
            label_visibility="hidden",
            value=interview_notes_to_display.content,
            key=f"interview_notes_{interview_notes_to_display.id}_content",
            height=150,
        )
        save_btn_col, delete_btn_col = st.columns(2, width=350)
        with save_btn_col:
            if st.button(
                "Save Changes",
                key=f"save_interview_notes_{interview_notes_to_display.id}",
            ):
                try:
                    interview_notes_repo.update(interview_notes_to_display.id, title=new_title, content=new_content)  # type: ignore[arg-type]
                    st.toast("interview notes updated successfully!")
                    st.rerun()
                except Exception as e:
                    disappearing_message(
                        st=st,
                        message="Error updating interview notes",
                        msg_type="error",
                        duration=3,
                    )
                    st.error(f"Error updating interview notes: {str(e)}")
        with delete_btn_col:
            if st.button("Delete", key=f"delete_interview_notes_{interview_notes_to_display.id}"):  # type: ignore[call-arg]
                try:
                    interview_notes_repo.delete(interview_notes_to_display.id)  # type: ignore[arg-type]
                    st.toast("interview notes deleted successfully!")
                    st.rerun()
                except Exception as e:
                    disappearing_message(
                        st=st,
                        message="Error deleting interview notes",
                        msg_type="error",
                        duration=3,
                    )
