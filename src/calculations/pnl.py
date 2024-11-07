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
