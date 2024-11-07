# src/calculations/pnl.py

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

def long_call_calculator(price_per_option, contracts, strike_price, current_price):
    total_cost = price_per_option * contracts * 100
    max_risk = total_cost  # Maximum risk is the cost of buying the call
    breakeven = strike_price + (price_per_option / 100)
    probability_of_profit = None  # Placeholder, requires complex calculations or data sources

    return {
        "total_cost": total_cost,
        "max_risk": max_risk,
        "breakeven": breakeven,
        "probability_of_profit": probability_of_profit
    }
