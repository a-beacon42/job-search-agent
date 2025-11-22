import streamlit as st
from pathlib import Path

st.markdown("under construction -- future home will look something like:")
img_path = Path(__file__).parent.parent / "static" / "images" / "future_home.jpeg"
st.image(image=img_path)
