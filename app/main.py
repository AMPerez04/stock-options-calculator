# app/main_app.py

import sys
import os

# Add the project root directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
if project_root not in sys.path:
    sys.path.append(project_root)

# Now, proceed with other imports
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
from dateutil import parser

def calculate_time_to_expiry(expiration_date):
    current_date = datetime.now()
    exp_date = parser.parse(expiration_date)
    delta = exp_date - current_date
    T = delta.days / 365  # Time to expiry in years
    return max(T, 0.001)  # Prevent division by zero or negative values

# Import custom modules
from components.option_inputs import stock_symbol_input
from src.calculations.pnl import long_call_calculator
from app.plotting import plot_pnl_chart, price_profit_table

from src.data.data_fetch import get_real_time_price, get_option_chain

def display_option_chain_as_table(symbol, expiration_date):
    """
    Displays the option chain for the given symbol and expiration date.
    Allows users to select specific Call or Put options.
    """
    # Retrieve the option chain for the selected expiration date
    calls, puts = get_option_chain(symbol, expiration_date)

    if calls is not None and puts is not None:
        st.subheader(f"Option Chain for {symbol} - Expiration: {expiration_date}")
        
        # Display calls and puts as non-clickable tables for reference
        st.write("### Calls")
        st.dataframe(calls[['strike', 'bid', 'ask', 'lastPrice', 'volume', 'openInterest', 'impliedVolatility']], height=300)
        
        st.write("### Puts")
        st.dataframe(puts[['strike', 'bid', 'ask', 'lastPrice', 'volume', 'openInterest', 'impliedVolatility']], height=300)
        
        # Interactive section to select option details
        st.sidebar.subheader("Select Option")
        
        # Radio button to choose between Call and Put
        option_type = st.sidebar.radio("Option Type", ["Call", "Put"], key="option_type_radio")
        
        if option_type == "Call":
            # Select strike and price for call options
            selected_call_strike = st.sidebar.selectbox(
                "Call Strike Price", 
                options=calls['strike'].tolist(), 
                key="selected_call_strike"
            )
            selected_call_price_type = st.sidebar.selectbox(
                "Select Call Price Type", 
                options=['bid', 'ask', 'lastPrice'], 
                key="selected_call_price_type"
            )
            selected_call_price = calls.loc[calls['strike'] == selected_call_strike, selected_call_price_type].values[0]
            selected_call_iv = calls.loc[calls['strike'] == selected_call_strike, 'impliedVolatility'].values[0]
            
            # Callback function for updating session state
            def set_selected_call_option():
                st.session_state['strike_price'] = selected_call_strike
                st.session_state['price_per_option'] = selected_call_price
                st.session_state['implied_volatility'] = selected_call_iv
                st.session_state['option_type'] = 'call'
                st.session_state['show_option_chain'] = False  # Hide option chain after selection
                st.sidebar.success(f"**Selected Call Option:**\n**Strike Price:** {selected_call_strike}\n**Price per Option:** ${selected_call_price:.2f}\n**Implied Volatility:** {selected_call_iv*100:.2f}%")
    
            # Button to update session state with selected call option
            st.sidebar.button("Use Selected Call Option", key="use_call_option", on_click=set_selected_call_option)
        
        elif option_type == "Put":
            # Select strike and price for put options
            selected_put_strike = st.sidebar.selectbox(
                "Put Strike Price", 
                options=puts['strike'].tolist(), 
                key="selected_put_strike"
            )
            selected_put_price_type = st.sidebar.selectbox(
                "Select Put Price Type", 
                options=['bid', 'ask', 'lastPrice'], 
                key="selected_put_price_type"
            )
            selected_put_price = puts.loc[puts['strike'] == selected_put_strike, selected_put_price_type].values[0]
            selected_put_iv = puts.loc[puts['strike'] == selected_put_strike, 'impliedVolatility'].values[0]
            
            # Callback function for updating session state
            def set_selected_put_option():
                st.session_state['strike_price'] = selected_put_strike
                st.session_state['price_per_option'] = selected_put_price
                st.session_state['implied_volatility'] = selected_put_iv
                st.session_state['option_type'] = 'put'
                st.session_state['show_option_chain'] = False  # Hide option chain after selection
                st.sidebar.success(f"**Selected Put Option:**\n**Strike Price:** {selected_put_strike}\n**Price per Option:** ${selected_put_price:.2f}\n**Implied Volatility:** {selected_put_iv*100:.2f}%")
    
            # Button to update session state with selected put option
            st.sidebar.button("Use Selected Put Option", key="use_put_option", on_click=set_selected_put_option)

def display_chart_and_table(symbol, strike_price, price_per_option, contracts, implied_volatility, expiration_date):
    """
    Displays the P&L chart, day-by-day chart, and the price-profit table based on the input parameters.
    """
    T = calculate_time_to_expiry(expiration_date)
    
    # Define a reasonable price range around the strike price
    price_range = np.linspace(strike_price * 0.7, strike_price * 1.3, 100)
    
    # Calculate P&L for each price in the range
    pnl = []
    for price in price_range:
        result = long_call_calculator(price_per_option, contracts, strike_price, price, implied_volatility, time_to_expiry=T)
        pnl.append(result['pnl'])
    
    # Create DataFrame for plotting
    df_pnl = pd.DataFrame({
        'Stock Price at Expiry': price_range,
        'P&L': pnl
    })
    
    # Plot P&L Chart
    fig_pnl = px.line(df_pnl, x='Stock Price at Expiry', y='P&L', title='P&L vs. Stock Price at Expiry')
    st.plotly_chart(fig_pnl, use_container_width=True)
    
    # Day-by-Day P&L Simulation
    days = 30
    daily_pnl = []
    daily_prices = np.linspace(strike_price * 0.7, strike_price * 1.3, days)
    
    for day, price in enumerate(daily_prices, start=1):
        result = long_call_calculator(price_per_option, contracts, strike_price, price, implied_volatility, time_to_expiry=T)
        daily_pnl.append(result['pnl'])
    
    df_daily_pnl = pd.DataFrame({
        'Day': range(1, days + 1),
        'Stock Price': daily_prices,
        'P&L': daily_pnl
    })
    
    # Plot Day-by-Day P&L Chart
    fig_daily_pnl = px.line(df_daily_pnl, x='Day', y='P&L', title='Day-by-Day P&L Simulation')
    st.plotly_chart(fig_daily_pnl, use_container_width=True)
    
    # Display Price-Profit Table
    st.subheader("Price-Profit Table")
    st.write(df_pnl)

def display_calculator(symbol, strike_price, price_per_option, contracts, current_price, implied_volatility, expiration_date):
    """
    Calculates and displays the estimated returns for a long call position.
    """
    T = calculate_time_to_expiry(expiration_date)
    results = long_call_calculator(price_per_option, contracts, strike_price, current_price, implied_volatility, time_to_expiry=T)
    
    st.subheader("Estimated Returns")
    st.write(f"**Entry Cost:** ${results['total_cost']:.2f}")
    st.write(f"**Maximum Risk:** ${results['max_risk']:.2f}")
    st.write(f"**Breakeven at Expiry:** ${results['breakeven']:.2f}")
    
    if results['probability_of_profit'] is not None:
        st.write(f"**Probability of Profit:** {results['probability_of_profit']:.2f}%")
    else:
        st.write("**Probability of Profit:** Calculation not available")


def main():
    # Configure the Streamlit page
    st.set_page_config(page_title="American Options Calculator", layout="wide")
    st.title("🏦 American Options Calculator")

    # Initialize session state variables
    if 'strike_price' not in st.session_state:
        st.session_state['strike_price'] = 100.0
    if 'price_per_option' not in st.session_state:
        st.session_state['price_per_option'] = 3.40
    if 'option_type' not in st.session_state:
        st.session_state['option_type'] = None
    if 'show_option_chain' not in st.session_state:
        st.session_state['show_option_chain'] = False
    if 'symbol' not in st.session_state:
        st.session_state['symbol'] = ''
    if 'expiration_date' not in st.session_state:
        st.session_state['expiration_date'] = ''
    if 'implied_volatility' not in st.session_state:
        st.session_state['implied_volatility'] = 0.0

    # Sidebar for stock symbol input
    symbol = stock_symbol_input()
    
    # Check if symbol has changed
    if symbol != st.session_state['symbol']:
        st.session_state['show_option_chain'] = False
        st.session_state['symbol'] = symbol
        st.session_state['expiration_date'] = ''
        st.session_state['option_type'] = None
        st.session_state['implied_volatility'] = 0.0

    if symbol:
        # Fetch real-time stock price
        current_price = get_real_time_price(symbol)
        if current_price:
            st.sidebar.markdown(f"### Current Price of {symbol}: ${current_price:.2f}")
        else:
            st.sidebar.error("Failed to retrieve current stock price.")

        # Fetch expiration dates
        stock = yf.Ticker(symbol)
        expiration_dates = stock.options  # List of expiration dates

        if expiration_dates:
            expiration_date = st.sidebar.selectbox("Select Expiration Date", expiration_dates, key="expiration_date_select")

            # Check if expiration date has changed
            if expiration_date != st.session_state['expiration_date']:
                st.session_state['show_option_chain'] = False
                st.session_state['expiration_date'] = expiration_date
                st.session_state['option_type'] = None
                st.session_state['implied_volatility'] = 0.0

            # Callback function to set 'show_option_chain' to True
            def show_option_chain_callback():
                st.session_state['show_option_chain'] = True

            # Button to show option chain
            st.sidebar.button("Show Option Chain", key="show_option_chain_btn", on_click=show_option_chain_callback)

            # Display the option chain if 'show_option_chain' is True
            if st.session_state['show_option_chain']:
                display_option_chain_as_table(symbol, expiration_date)

        else:
            st.sidebar.error("No expiration dates available for the selected symbol.")

        # Input Mode Selection
        input_mode = st.sidebar.radio("Choose Input Mode", ["Auto-fill", "Manual Input"])

        st.sidebar.subheader("Option Details")

        # Option details based on input mode
        if input_mode == "Auto-fill":
            # Auto-fill using session state
            strike_price = st.session_state['strike_price']
            price_per_option = st.session_state['price_per_option']
            implied_volatility = st.session_state['implied_volatility']
            option_type = st.session_state.get('option_type', None)
            if option_type:
                st.sidebar.markdown(f"**Selected Option Type:** {option_type.capitalize()}")
                st.sidebar.markdown(f"**Strike Price:** {strike_price}")
                st.sidebar.markdown(f"**Price per Option:** ${price_per_option:.2f}")
                st.sidebar.markdown(f"**Implied Volatility:** {implied_volatility*100:.2f}%")
            else:
                st.sidebar.info("Please select a call or put option from the option chain.")
        else:
            # Manual input
            strike_price = st.sidebar.number_input(
                "Strike Price", 
                min_value=0.0, 
                value=st.session_state['strike_price'], 
                step=1.0,
                key="manual_strike_price"
            )
            price_per_option = st.sidebar.number_input(
                "Price per Option", 
                min_value=0.0, 
                value=st.session_state['price_per_option'], 
                step=0.01,
                key="manual_price_per_option"
            )
            implied_volatility = st.sidebar.number_input(
                "Implied Volatility (%)", 
                min_value=0.0, 
                max_value=500.0, 
                value=st.session_state['implied_volatility'] * 100, 
                step=0.1,
                key="manual_implied_volatility"
            ) / 100.0  # Convert to decimal

        # Contracts input (common to both modes)
        contracts = st.sidebar.number_input("Number of Contracts", min_value=1, value=1, step=1)

        # Callback function to calculate and display results
        def calculate_long_call_callback():
            if input_mode == "Auto-fill":
                option_type = st.session_state.get('option_type', None)
                if option_type is None:
                    st.sidebar.error("Please select a call or put option from the option chain before calculating.")
                else:
                    expiration_date = st.session_state['expiration_date']
                    display_calculator(
                        symbol, 
                        st.session_state['strike_price'], 
                        st.session_state['price_per_option'], 
                        contracts, 
                        current_price,
                        st.session_state['implied_volatility'],
                        expiration_date  # Pass expiration_date here
                    )
                    display_chart_and_table(
                        symbol, 
                        st.session_state['strike_price'], 
                        st.session_state['price_per_option'], 
                        contracts,
                        st.session_state['implied_volatility'],
                        expiration_date  # Pass expiration_date here
                    )
            else:
                if current_price:
                    # Update session state with manual inputs
                    st.session_state['strike_price'] = strike_price
                    st.session_state['price_per_option'] = price_per_option
                    st.session_state['implied_volatility'] = implied_volatility
                    st.session_state['option_type'] = 'manual'
                    expiration_date = st.session_state['expiration_date']
                    display_calculator(
                        symbol, 
                        strike_price, 
                        price_per_option, 
                        contracts, 
                        current_price,
                        implied_volatility,
                        expiration_date  # Pass expiration_date here
                    )
                    display_chart_and_table(
                        symbol, 
                        strike_price, 
                        price_per_option, 
                        contracts,
                        implied_volatility,
                        expiration_date  # Pass expiration_date here
                    )
                else:
                    st.sidebar.error("Cannot perform calculations without current stock price.")

        # Button to calculate long call
        st.sidebar.button("Calculate Long Call", key="calculate_long_call_btn", on_click=calculate_long_call_callback)

        # Optional: Display current session state for debugging
        # Remove or comment out in production
        with st.expander("🔍 Debugging Information"):
            st.write("### Session State")
            st.write(st.session_state)

if __name__ == "__main__":
    main()
