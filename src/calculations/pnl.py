# src/calculations/pnl.py

from scipy.stats import norm
import numpy as np

def calculate_pnl(position, initial_premium, current_premium, quantity=1):
    """
    Calculate P&L for an option position.

    Parameters:
    position : str
        'long' or 'short'
    initial_premium : float
        The premium paid (for long) or received (for short) when entering the position
    current_premium : float
        The current premium of the option
    quantity : int
        Number of contracts (each contract typically represents 100 shares)

    Returns:
    pnl : float
        Profit or loss
    """
    if position.lower() == 'long':
        pnl = (current_premium - initial_premium) * quantity * 100
    elif position.lower() == 'short':
        pnl = (initial_premium - current_premium) * quantity * 100
    else:
        raise ValueError("position must be 'long' or 'short'")

    return pnl


def long_call_calculator(price_per_option, contracts, strike_price, current_price, implied_volatility, risk_free_rate=0.01, time_to_expiry=1):
    """
    Calculates the P&L for a long call option position.

    Parameters:
    - price_per_option: Premium paid per option
    - contracts: Number of contracts (1 contract = 100 options)
    - strike_price: Strike price of the option
    - current_price: Current stock price
    - implied_volatility: Implied volatility (as a decimal, e.g., 0.2 for 20%)
    - risk_free_rate: Annual risk-free interest rate (default 1%)
    - time_to_expiry: Time to expiry in years (default 1 year)

    Returns:
    A dictionary with total cost, max risk, breakeven, P&L, and probability of profit.
    """
    S = current_price
    K = strike_price
    sigma = implied_volatility
    r = risk_free_rate
    T = time_to_expiry
    N = contracts * 100  # Total number of options

    # Calculate d2
    d2 = (np.log(S / K) + (r - 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

    # Probability of Profit
    prob_profit = norm.cdf(d2) * 100  # Convert to percentage

    # Breakeven Point
    breakeven = K + price_per_option

    # Total Cost
    total_cost = price_per_option * N

    # Maximum Risk
    max_risk = total_cost

    # P&L at Expiry
    pnl = max(S - K, 0) * N - total_cost

    return {
        'total_cost': total_cost,
        'max_risk': max_risk,
        'breakeven': breakeven,
        'pnl': pnl,
        'probability_of_profit': prob_profit
    }