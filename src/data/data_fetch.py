# src/data/data_fetch.py

import yfinance as yf
import streamlit as st

def get_real_time_price(ticker):
    """
    Fetches the latest closing price of the specified ticker.

    Parameters:
    ticker : str
        Stock ticker symbol (e.g., 'AAPL')

    Returns:
    float
        Latest closing stock price
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        price = data['Close'].iloc[-1]
        return price
    except Exception as e:
        st.error(f"Error fetching real-time price for {ticker}: {e}")
        return None

def get_option_chain(ticker, expiration_date):
    """
    Fetches the option chain for the specified ticker and expiration date.

    Parameters:
    ticker : str
        Stock ticker symbol (e.g., 'AAPL')
    expiration_date : str
        Expiration date in 'YYYY-MM-DD' format

    Returns:
    pandas.DataFrame, pandas.DataFrame
        Calls and puts DataFrames
    """
    try:
        stock = yf.Ticker(ticker)
        option_chain = stock.option_chain(expiration_date)
        return option_chain.calls, option_chain.puts
    except Exception as e:
        st.error(f"Error fetching option chain for {ticker} on {expiration_date}: {e}")
        return None, None
