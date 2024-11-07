# app/components/option_inputs.py

import streamlit as st
import yfinance as yf

def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period='1d')
    return data['Close'].iloc[-1] if not data.empty else None

def stock_symbol_input():
    symbol = st.sidebar.text_input("Symbol", value="TSLA").upper()
    if symbol:
        price = get_stock_price(symbol)
        if price:
            st.sidebar.write(f"Current price: ${price:.2f}")
        else:
            st.sidebar.error("Stock not found. Please enter a valid symbol.")
    return symbol

def option_chain_selection(symbol):
    stock = yf.Ticker(symbol)
    expiration_dates = stock.options  # List of expiration dates
    expiration = st.sidebar.selectbox("Select expiration date", expiration_dates)

    # Retrieve option chain for the selected expiration date
    if expiration:
        option_chain = stock.option_chain(expiration)
        calls = option_chain.calls
        puts = option_chain.puts
        return calls, puts
    return None, None

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
        help="Enter the current price of the underlying stock.",
        key="stock_price_input"
    )
    K = st.sidebar.number_input(
        "Strike Price (K)",
        min_value=0.0,
        value=100.0,
        step=1.0,
        format="%.2f",
        help="Enter the strike price of the option.",
        key="strike_price_input"
    )
    T = st.sidebar.number_input(
        "Time to Expiration (Years)",
        min_value=0.0,
        value=1.0,
        step=0.1,
        format="%.2f",
        help="Enter the time to expiration in years (e.g., 0.5 for 6 months).",
        key="time_to_expiration_input"
    )
    r = st.sidebar.number_input(
        "Risk-Free Rate (r)",
        min_value=0.0,
        max_value=1.0,
        value=0.05,
        step=0.01,
        format="%.4f",
        help="Enter the annual risk-free interest rate (e.g., 0.05 for 5%).",
        key="risk_free_rate_input"
    )
    sigma = st.sidebar.number_input(
        "Volatility (σ)",
        min_value=0.0,
        max_value=5.0,
        value=0.2,
        step=0.01,
        format="%.4f",
        help="Enter the annual volatility of the underlying stock (e.g., 0.2 for 20%).",
        key="volatility_input"
    )
    option_type = st.sidebar.selectbox(
        "Option Type",
        ["call", "put"],
        help="Select the type of option.",
        key="option_type_select"
    )
    american = st.sidebar.checkbox(
        "American Option",
        value=True,
        help="Check if the option is American; uncheck for European.",
        key="american_option_checkbox"
    )
    N = st.sidebar.slider(
        "Number of Time Steps (N)",
        min_value=10,
        max_value=1000,
        value=100,
        step=10,
        help="Select the number of time steps for the Binomial Model (higher for more accuracy).",
        key="time_steps_slider"
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
