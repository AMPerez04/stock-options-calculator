# app.py

import streamlit as st
import yfinance as yf
import pandas as pd

# Import custom modules
from components.option_inputs import get_option_parameters, stock_symbol_input, option_chain_selection
from components.position_inputs import get_position_parameters
from src.pricing.binomial_model import binomial_option_price
from src.calculations.pnl import calculate_pnl, long_call_calculator
from app.plotting import plot_pnl_vs_stock, plot_pnl_chart, price_profit_table
from src.data.data_fetch import get_real_time_price, get_option_chain

def display_option_chain_as_table(symbol, expiration_date):
    """
    Displays the option chain for the given symbol and expiration date.
    Allows users to select specific call and put options.
    """
    # Retrieve the option chain for the selected expiration date
    calls, puts = get_option_chain(symbol, expiration_date)

    if calls is not None and puts is not None:
        st.subheader(f"Option Chain for {symbol} - Expiration: {expiration_date}")
        
        # Display calls and puts as non-clickable tables for reference
        st.write("### Calls")
        st.dataframe(calls[['strike', 'bid', 'ask', 'lastPrice', 'volume', 'openInterest']], height=300)
        
        st.write("### Puts")
        st.dataframe(puts[['strike', 'bid', 'ask', 'lastPrice', 'volume', 'openInterest']], height=300)
        
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
            
            # Callback function for updating session state
            def set_selected_call_option():
                st.session_state['strike_price'] = selected_call_strike
                st.session_state['price_per_option'] = selected_call_price
                st.session_state['option_type'] = 'call'
                st.session_state['show_option_chain'] = False  # Hide option chain after selection
                st.sidebar.success(f"Selected Call Option:\n**Strike Price:** {selected_call_strike}\n**Price per Option:** ${selected_call_price}")
        
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
            
            # Callback function for updating session state
            def set_selected_put_option():
                st.session_state['strike_price'] = selected_put_strike
                st.session_state['price_per_option'] = selected_put_price
                st.session_state['option_type'] = 'put'
                st.session_state['show_option_chain'] = False  # Hide option chain after selection
                st.sidebar.success(f"Selected Put Option:\n**Strike Price:** {selected_put_strike}\n**Price per Option:** ${selected_put_price}")
        
            # Button to update session state with selected put option
            st.sidebar.button("Use Selected Put Option", key="use_put_option", on_click=set_selected_put_option)

    else:
        st.error("Failed to retrieve option chain data.")

    return calls, puts

def display_chart_and_table(symbol, strike_price, price_per_option, contracts):
    """
    Displays the P&L chart and the price-profit table based on the input parameters.
    """
    # Define a reasonable price range around the strike price
    price_range = range(int(strike_price * 0.8), int(strike_price * 1.2) + 1, 1)
    
    plot_pnl_chart(strike_price, price_per_option, contracts, price_range)
    price_profit_table(strike_price, price_per_option, contracts, price_range)

def display_calculator(symbol, strike_price, price_per_option, contracts, current_price):
    """
    Calculates and displays the estimated returns for a long call position.
    """
    results = long_call_calculator(price_per_option, contracts, strike_price, current_price)
    
    st.subheader("Estimated Returns")
    st.write(f"**Entry Cost:** ${results['total_cost']:.2f}")
    st.write(f"**Maximum Risk:** ${results['max_risk']:.2f}")
    st.write(f"**Breakeven at Expiry:** ${results['breakeven']:.2f}")
    
    if results['probability_of_profit'] is not None:
        st.write(f"**Probability of Profit:** {results['probability_of_profit']}%")
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

    # Sidebar for stock symbol input
    symbol = stock_symbol_input()
    
    # Check if symbol has changed
    if symbol != st.session_state['symbol']:
        st.session_state['show_option_chain'] = False
        st.session_state['symbol'] = symbol
        st.session_state['expiration_date'] = ''

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

            # Callback function to set 'show_option_chain' to True
            def show_option_chain_callback():
                st.session_state['show_option_chain'] = True

            # Button to show option chain
            st.sidebar.button("Show Option Chain", key="show_option_chain_btn", on_click=show_option_chain_callback)

            # Display the option chain if 'show_option_chain' is True
            if st.session_state['show_option_chain']:
                calls, puts = display_option_chain_as_table(symbol, expiration_date)

        else:
            st.sidebar.error("No expiration dates available for the selected symbol.")

        # Input Mode Selection
        input_mode = st.sidebar.radio("Choose Input Mode", ["Auto-fill", "Manual Input"])

        st.sidebar.subheader("Call/Put Option Details")

        # Option details based on input mode
        if input_mode == "Auto-fill":
            # Auto-fill using session state
            strike_price = st.session_state['strike_price']
            price_per_option = st.session_state['price_per_option']
            option_type = st.session_state.get('option_type', None)
            if option_type:
                st.sidebar.markdown(f"**Selected Option Type:** {option_type.capitalize()}")
                st.sidebar.markdown(f"**Strike Price:** {strike_price}")
                st.sidebar.markdown(f"**Price per Option:** ${price_per_option}")
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

        # Contracts input (common to both modes)
        contracts = st.sidebar.number_input("Number of Contracts", min_value=1, value=1, step=1)

        # Callback function to calculate and display results
        def calculate_long_call_callback():
            if input_mode == "Auto-fill":
                option_type = st.session_state.get('option_type', None)
                if option_type is None:
                    st.sidebar.error("Please select a call or put option from the option chain before calculating.")
                else:
                    display_calculator(symbol, st.session_state['strike_price'], st.session_state['price_per_option'], contracts, current_price)
                    display_chart_and_table(symbol, st.session_state['strike_price'], st.session_state['price_per_option'], contracts)
            else:
                if current_price:
                    # Update session state with manual inputs
                    st.session_state['strike_price'] = strike_price
                    st.session_state['price_per_option'] = price_per_option
                    st.session_state['option_type'] = 'manual'
                    display_calculator(symbol, strike_price, price_per_option, contracts, current_price)
                    display_chart_and_table(symbol, strike_price, price_per_option, contracts)
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
