# app/components/option_inputs.py

import streamlit as st

def get_option_parameters():
    """
    Collects option parameters from the user via Streamlit sidebar.

    Returns:
        dict: A dictionary containing option parameters.
    """
    S = st.sidebar.number_input(
        "Current Stock Price (S)",
        min_value=0.0,
        value=100.0,
        step=1.0,
        format="%.2f",
        help="Enter the current price of the underlying stock."
    )
    K = st.sidebar.number_input(
        "Strike Price (K)",
        min_value=0.0,
        value=100.0,
        step=1.0,
        format="%.2f",
        help="Enter the strike price of the option."
    )
    T = st.sidebar.number_input(
        "Time to Expiration (Years)",
        min_value=0.0,
        value=1.0,
        step=0.1,
        format="%.2f",
        help="Enter the time to expiration in years (e.g., 0.5 for 6 months)."
    )
    r = st.sidebar.number_input(
        "Risk-Free Rate (r)",
        min_value=0.0,
        max_value=1.0,
        value=0.05,
        step=0.01,
        format="%.4f",
        help="Enter the annual risk-free interest rate (e.g., 0.05 for 5%)."
    )
    sigma = st.sidebar.number_input(
        "Volatility (σ)",
        min_value=0.0,
        max_value=5.0,
        value=0.2,
        step=0.01,
        format="%.4f",
        help="Enter the annual volatility of the underlying stock (e.g., 0.2 for 20%)."
    )
    option_type = st.sidebar.selectbox(
        "Option Type",
        ["call", "put"],
        help="Select the type of option."
    )
    american = st.sidebar.checkbox(
        "American Option",
        value=True,
        help="Check if the option is American; uncheck for European."
    )
    N = st.sidebar.slider(
        "Number of Time Steps (N)",
        min_value=10,
        max_value=1000,
        value=100,
        step=10,
        help="Select the number of time steps for the Binomial Model (higher for more accuracy)."
    )

    return {
        "S": S,
        "K": K,
        "T": T,
        "r": r,
        "sigma": sigma,
        "option_type": option_type,
        "american": american,
        "N": N
    }
