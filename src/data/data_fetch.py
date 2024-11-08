# src/data/data_fetch.py

import yfinance as yf
import streamlit as st
import pandas as pd

@st.cache_data
def get_real_time_price(symbol):
    """
    Fetches the real-time stock price for the given symbol.
    """
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period='1d')
        current_price = data['Close'].iloc[-1]
        return current_price
    except Exception as e:
        st.error(f"Error fetching real-time price: {e}")
        return None

@st.cache_data
def get_option_chain(symbol, expiration_date):
    """
    Fetches the option chain for the given symbol and expiration date.
    Returns separate DataFrames for calls and puts, including implied volatility.
    """
    try:
        stock = yf.Ticker(symbol)
        opt_chain = stock.option_chain(expiration_date)
        calls = opt_chain.calls
        puts = opt_chain.puts
        return calls, puts
    except Exception as e:
        st.error(f"Error fetching option chain: {e}")
        return None, None