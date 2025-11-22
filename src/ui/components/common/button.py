import streamlit as st


def primary_button(label):
    return st.markdown(
        f"""
        <div class="stButton">
            <button>{label}</button>
        </div>
        """,
        unsafe_allow_html=True,
    )
