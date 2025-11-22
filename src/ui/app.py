import streamlit as st
import sys
import os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_css():
    css_path = Path(__file__).parent / "styles" / "theme.css"
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()


def main():

    pages = [
        st.Page("./pages/home.py", title="home", icon=":material/home:"),
        st.Page("./pages/new_jobs.py", title="new jobs", icon=":material/work_alert:"),
    ]
    page = st.navigation(pages)
    page.run()


if __name__ == "__main__":
    main()
