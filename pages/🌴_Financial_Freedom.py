import streamlit as st
import datetime
from collections import namedtuple

st.set_page_config(
    page_title="Financial Calculators",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded",
)

def financial_freedom_years(balance, interest_rate, yearly_expenses, yearly_addition, current_age, depreciation_rate=0.02):
    """
    Calculate the number of years it will take for a person to be financially free.

    Parameters:
    balance (float): The user's current invested balance.
    interest_rate (float): The annual interest rate.
    depreciation_rate (float): The annual depreciation rate.
    yearly_expenses (float): The person's annual expenses.
    yearly_addition (float): The amount added to investments each year.
    current_age (float): The person's current age.

    Returns:
    NamedTuple: A named tuple containing the current year, years, and balance.
    """
    # use datetime to get current year
    current_year = datetime.datetime.now().year
    # Calculate the real interest rate taking into account the annual depreciation and inflation
    real_interest_rate = (1 + interest_rate) / (1 + depreciation_rate) - 1

    years = 0
    age_history = []
    balance_history = [] 
    while balance < yearly_expenses / real_interest_rate:
        balance = balance * (1 + real_interest_rate) + yearly_addition
        balance_history.append(balance)
        current_year += 1
        years += 1
        age_history.append(current_age + years)

    # format balance to be a dollar amount
    balance = "${:,.2f}".format(balance)
    # create a named tuple for current_year, years, balance so that it prints with the names
    FinancialFreedom = namedtuple('FinancialFreedom', ['payoff_year', 'years', 'balance','balance_history', 'age_history'])
    return FinancialFreedom(current_year, years, balance, balance_history, age_history)
st.title("Financial Freedom Calculator")

# Use st.sidebar for inputs
balance = st.sidebar.number_input("Enter your current invested balance", min_value=0, value=100000)
interest_rate = st.sidebar.number_input("Enter the annual interest rate", min_value=0.0, value=0.08)
yearly_expenses = st.sidebar.number_input("Enter your annual expenses during retirement", min_value=0, value=85000)
yearly_addition = st.sidebar.number_input("Enter the amount added to investments each year", min_value=0, value=10000)
current_age = st.sidebar.number_input("Enter your current age", min_value=0, value=25)

if st.sidebar.button("Calculate"):  
    results = financial_freedom_years(balance, interest_rate, yearly_expenses, yearly_addition, current_age)  
    st.write(f"Year of Financial Freedom: {results.payoff_year}")  
    st.write(f"Years until Financial Freedom: {results.years}")
    st.write(f"Age of Financial Freedom: {results.years + current_age}")
    st.write(f"Final Balance: {results.balance}")  
  
    st.line_chart(
        data=dict(
            age_history=results.age_history,
            balance_history=results.balance_history,
        )
    )

    # Advertisement  
    # ad_html = """  
    # <div style="padding:10px; color:white; background-color:blue;">  
    # <h3>Your Advertisement Here</h3>  
    # <p>This is an example of how you could place an advertisement in your Streamlit app.</p>  
    # </div>  
    # """  
    # st.markdown(ad_html, unsafe_allow_html=True) 

    