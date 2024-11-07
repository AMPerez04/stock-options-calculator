# app/main.py

import sys
import os
import streamlit as st
import yfinance as yf

# Add the root directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(root_dir)

from components.option_inputs import get_option_parameters, stock_symbol_input, option_chain_selection
from components.position_inputs import get_position_parameters
from src.pricing.binomial_model import binomial_option_price
from src.calculations.pnl import calculate_pnl, long_call_calculator
from app.plotting import plot_pnl_vs_stock, plot_pnl_chart, price_profit_table
from src.data.data_fetch import get_real_time_price, get_option_chain

def display_option_chain(symbol, expiration_date):
    # Retrieve the option chain for the selected expiration date
    calls, puts = get_option_chain(symbol, expiration_date)
    
    if calls is not None and puts is not None:
        st.subheader(f"Option Chain for {symbol} - Expiration: {expiration_date}")
        
        # Display calls and puts in two separate tables
        st.write("### Calls")
        st.dataframe(calls[['strike', 'bid', 'ask', 'lastPrice', 'volume', 'openInterest']])
        
        st.write("### Puts")
        st.dataframe(puts[['strike', 'bid', 'ask', 'lastPrice', 'volume', 'openInterest']])

def display_chart_and_table(symbol, strike_price, price_per_option, contracts):
    price_range = range(int(strike_price * 0.9), int(strike_price * 1.1), 1)
    plot_pnl_chart(strike_price, price_per_option, contracts, price_range)
    price_profit_table(strike_price, price_per_option, contracts, price_range)

def display_calculator(symbol, strike_price, price_per_option, contracts, current_price):
    results = long_call_calculator(price_per_option, contracts, strike_price, current_price)
    
    st.subheader("Estimated returns")
    st.write(f"Entry cost: ${results['total_cost']}")
    st.write(f"Maximum risk: ${results['max_risk']}")
    st.write(f"Breakeven at expiry: ${results['breakeven']}")
    if results['probability_of_profit'] is not None:
        st.write(f"Probability of profit: {results['probability_of_profit']}%")
    else:
        st.write("Probability of profit: Calculation not available")
def main():
    st.set_page_config(page_title="American Options Calculator", layout="wide")
    st.title("🏦 American Options Calculator")

    # Sidebar for stock symbol and option inputs
    symbol = stock_symbol_input()
    if symbol:
        current_price = get_real_time_price(symbol)
        if current_price:
            st.sidebar.write(f"Current Price of {symbol}: ${current_price:.2f}")

        # Fetch and display expiration dates for the option chain
        stock = yf.Ticker(symbol)
        expiration_dates = stock.options  # List of expiration dates
        
        expiration_date = st.sidebar.selectbox("Select Expiration Date", expiration_dates)
        
        # Display button to show option chain
        if st.sidebar.button("Show Option Chain"):
            display_option_chain(symbol, expiration_date)
        
        # Option details for call calculator
        st.sidebar.subheader("Call Calculator")
        strike_price = st.sidebar.number_input("Strike Price", min_value=0.0, value=100.0, step=1.0)
        price_per_option = st.sidebar.number_input("Price per option", value=3.40)
        contracts = st.sidebar.number_input("Contracts", min_value=1, value=1)

        # Long Call Calculator Execution
        if st.sidebar.button("Calculate Long Call"):
            display_calculator(symbol, strike_price, price_per_option, contracts, current_price)
            display_chart_and_table(symbol, strike_price, price_per_option, contracts)

if __name__ == "__main__":
    main()