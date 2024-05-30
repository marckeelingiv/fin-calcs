import streamlit as st
## import environment variables
from os import getenv

google_adds_link = getenv("GOOGLE_ADDS_LINK")

st.set_page_config(
    page_title="Financial Calculators",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Financial Calculators")
st.sidebar.success("Welcome to the Financial Calculators!")

custom_html = f'<script async src="{google_adds_link}" crossorigin="anonymous"></script>'

st.markdown(custom_html, unsafe_allow_html=True)

st.write(custom_html)