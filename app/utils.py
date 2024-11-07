# app/utils.py

import streamlit as st

def format_currency(value):
    """
    Formats a numerical value as currency.

    Args:
        value (float): The numerical value to format.

    Returns:
        str: The formatted currency string.
    """
    return f"${value:,.2f}"

def display_error(message):
    """
    Displays an error message in Streamlit.

    Args:
        message (str): The error message to display.
    """
    st.error(message)

def display_success(message):
    """
    Displays a success message in Streamlit.

    Args:
        message (str): The success message to display.
    """
    st.success(message)
