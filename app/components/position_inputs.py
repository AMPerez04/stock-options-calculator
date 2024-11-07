# app/components/position_inputs.py

import streamlit as st

def get_position_parameters():
    """
    Collects position parameters from the user via Streamlit sidebar.

    Returns:
        dict: A dictionary containing position parameters.
    """
    position = st.sidebar.selectbox(
        "Position",
        ["long", "short"],
        help="Select whether you are buying (long) or selling (short) the option."
    )
    initial_premium = st.sidebar.number_input(
        "Initial Premium ($)",
        min_value=0.0,
        value=10.0,
        step=0.1,
        format="%.2f",
        help="Enter the premium paid (for long) or received (for short) when entering the position."
    )
    current_premium = st.sidebar.number_input(
        "Current Premium ($)",
        min_value=0.0,
        value=8.0,
        step=0.1,
        format="%.2f",
        help="Enter the current premium of the option."
    )
    quantity = st.sidebar.number_input(
        "Number of Contracts",
        min_value=1,
        value=1,
        step=1,
        help="Enter the number of option contracts (each contract typically represents 100 shares)."
    )

    return {
        "position": position,
        "initial_premium": initial_premium,
        "current_premium": current_premium,
        "quantity": int(quantity)
    }
