# app/plotting.py

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from src.pricing.binomial_model import binomial_option_price
from src.calculations.pnl import calculate_pnl

def plot_pnl_vs_stock(option_params, position_params):
    """
    Plots the Profit and Loss (P&L) against a range of underlying stock prices.

    Args:
        option_params (dict): Parameters for option pricing.
        position_params (dict): Parameters for position P&L calculation.
    """
    st.subheader("📊 P&L vs. Underlying Stock Price")

    # Define a range of stock prices (e.g., 50% to 150% of strike price)
    S_min = option_params['K'] * 0.5
    S_max = option_params['K'] * 1.5
    S_range = np.linspace(S_min, S_max, 100)

    pnl_values = []

    for S in S_range:
        # Update the stock price in option parameters
        current_option_params = option_params.copy()
        current_option_params['S'] = S

        # Calculate current premium using the binomial model
        current_premium = binomial_option_price(**current_option_params)

        # Update current premium in position parameters
        current_position_params = position_params.copy()
        current_position_params['current_premium'] = current_premium

        # Calculate P&L
        pnl = calculate_pnl(**current_position_params)
        pnl_values.append(pnl)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(S_range, pnl_values, label='P&L', color='blue')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.xlabel('Underlying Stock Price at Expiration (S)')
    plt.ylabel('Profit and Loss ($)')
    plt.title('Option P&L at Expiration')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
