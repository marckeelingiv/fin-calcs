import streamlit as st

st.set_page_config(
    page_title="Financial Calculators",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded",
)

def calculate_mortgage_payoff(original_loan, original_term_years, original_term_months, interest_rate, remaining_years, remaining_months, extra_payment=0, extra_payment_frequency="one-time"):
    """
    This function calculates the time to pay off a mortgage,
    the interest saved and time saved by contributing extra.

    Parameters:
        original_loan (float): The original loan amount
        original_term_years (int): The original loan term in years
        original_term_months (int): The original loan term in months
        interest_rate (float): The annual interest rate
        remaining_years (int): The remaining term in years
        remaining_months (int): The remaining term in months
        extra_payment (float): The extra payment amount (default is 0)
        extra_payment_frequency (str): The frequency of the extra payment (default is "one-time", can be "monthly")

    Returns:
        dict: A dictionary with the time to pay off the loan,
              the interest saved and time saved by contributing extra,
              the original and new mortgage balances and total interests over time
    """

        # Calculate total number of periods (in months)
    total_periods = original_term_years * 12 + original_term_months
    remaining_periods = remaining_years * 12 + remaining_months

    # Calculate monthly interest rate
    monthly_interest_rate = interest_rate / 12 / 100

    # Calculate monthly payment (without extra payments)
    denominator = (1 - (1 + monthly_interest_rate) ** - total_periods)
    monthly_payment = original_loan * monthly_interest_rate / denominator

    # Initialize balance and interest histories
    original_balance_history = [original_loan]
    new_balance_history = [original_loan]
    original_interest_history = [0]
    new_interest_history = [0]
    original_total_interest_paid = 0
    new_total_interest_paid = 0

    # Loop over each period
    for period in range(1, total_periods + 1):
        # Calculate interest and principal paid for Original
        original_interest_paid = original_balance_history[-1] * monthly_interest_rate
        original_total_interest_paid += original_interest_paid
        original_principal_paid = monthly_payment - original_interest_paid

        # Calculate new balances and update histories
        original_balance = original_balance_history[-1] - original_principal_paid
        original_balance_history.append(original_balance)
        original_interest_history.append(original_interest_history[-1] + original_interest_paid)

        # Calculate extra payment for this period
        if extra_payment_frequency == "monthly" or (extra_payment_frequency == "one-time" and period == 1):
            extra = extra_payment
        else:
            extra = 0

        # Calculate new interest and principal paid with extra payment
        new_interest_paid = new_balance_history[-1] * monthly_interest_rate
        new_total_interest_paid += new_interest_paid
        new_principal_paid = monthly_payment - new_interest_paid + extra

        # Calculate new balance with extra payment and update histories
        new_balance = max(new_balance_history[-1] - new_principal_paid - extra, 0)
        new_balance_history.append(new_balance)
        new_interest_history.append(new_interest_history[-1] + new_interest_paid)

    # Calculate total interest and time saved
    total_interest_saved = original_total_interest_paid-new_total_interest_paid
    total_time_saved = (original_balance_history.index(next(b for b in original_balance_history if b <= 0)) -
                        new_balance_history.index(next(b for b in new_balance_history if b <= 0)))

    # Return results in a dictionary
    return {
        "total_interest_saved": total_interest_saved,
        "total_time_saved": total_time_saved,
        "original_balance_history": original_balance_history,
        "new_balance_history": new_balance_history,
        "original_interest_history": original_interest_history,
        "new_interest_history": new_interest_history
    }

st.title("Mortgage Payoff Calculator")

# Input fields
original_loan = st.sidebar.number_input("Original Loan Amount", value=100000, step=1000)
original_term_years = st.sidebar.number_input("Original Loan Term (Years)", value=30, step=1)
original_term_months = st.sidebar.number_input("Original Loan Term (Months)", value=0, step=1)
interest_rate = st.sidebar.number_input("Interest Rate", value=5.0, step=0.01)
remaining_years = st.sidebar.number_input("Remaining Term (Years)", value=30, step=1)
remaining_months = st.sidebar.number_input("Remaining Term (Months)", value=0, step=1)
extra_payment = st.sidebar.number_input("Extra Payment", value=200.0, step=100.0)
extra_payment_frequency = st.sidebar.selectbox(
    label="Extra Payment Frequency",
    options=["monthly", "one-time"],
)

# Button to trigger current_age
if st.sidebar.button("Calculate"):
    result = calculate_mortgage_payoff(original_loan, original_term_years, original_term_months, interest_rate, remaining_years, remaining_months, extra_payment, extra_payment_frequency)
    st.write(f"Interest Saved: ${result['total_interest_saved']:.2f}")
    st.write(f"Time Saved: {result['total_time_saved']} months")

    st.line_chart(
        data=dict(
            original_balance_history=result['original_balance_history'],
            new_balance_history=result['new_balance_history'],
            original_interest_history=result['original_interest_history'],
            new_interest_history=result['new_interest_history'],
        )
    )

