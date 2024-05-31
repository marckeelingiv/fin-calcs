import streamlit as st
from app_resources.app_functions import add_script_to_header

st.set_page_config(
    page_title="Financial Calculators",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Financial Calculators")
st.sidebar.success("Welcome to the Financial Calculators!")

add_script_to_header()