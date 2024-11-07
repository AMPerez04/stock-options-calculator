# app/main.py

import sys
import os
import streamlit as st

# Add the root directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(root_dir)

from components.option_inputs import get_option_parameters
from components.position_inputs import get_position_parameters
from src.pricing.binomial_model import binomial_option_price
from src.calculations.pnl import calculate_pnl
from app.plotting import plot_pnl_vs_stock
from src.data.data_fetch import get_real_time_price, get_option_chain  # If implementing real-time data

def main():
    st.set_page_config(page_title="American Options Calculator", layout="wide")
    st.title("🏦 American Options Calculator")

    # Sidebar for inputs
    st.sidebar.header("Option Parameters")
    option_params = get_option_parameters()

    st.sidebar.header("Position Parameters")
    position_params = get_position_parameters()

    # Action Buttons
    action = st.sidebar.selectbox("Select Action", ["Calculate Option Price", "Calculate P&L", "Plot P&L vs. Stock Price"])

    if st.sidebar.button("Execute"):
        if action == "Calculate Option Price":
            price = binomial_option_price(**option_params)
            st.subheader("📈 Option Pricing")
            st.write(f"The Binomial price of the **{option_params['option_type'].capitalize()}** option is: **${price:.2f}**")
        
        elif action == "Calculate P&L":
            pnl = calculate_pnl(**position_params)
            st.subheader("💰 Profit and Loss (P&L)")
            st.write(f"The P&L for the **{position_params['position'].capitalize()}** position is: **${pnl:.2f}**")
        
        elif action == "Plot P&L vs. Stock Price":
            plot_pnl_vs_stock(option_params, position_params)
        
        else:
            st.warning("Please select a valid action.")

if __name__ == "__main__":
    main()
