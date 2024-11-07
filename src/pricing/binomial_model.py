# src/pricing/binomial_model.py

import numpy as np

def binomial_option_price(S, K, T, r, sigma, option_type='call', american=True, N=100):
    """
    Calculate American or European option price using the Binomial model.

    Parameters:
    S : float
        Current stock price
    K : float
        Strike price
    T : float
        Time to expiration in years
    r : float
        Risk-free interest rate (annual)
    sigma : float
        Volatility of the underlying stock (annual)
    option_type : str
        'call' or 'put'
    american : bool
        True for American option, False for European
    N : int
        Number of time steps

    Returns:
    price : float
        Option price
    """
    # Calculate parameters
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))  # Up factor
    d = 1 / u                        # Down factor
    p = (np.exp(r * dt) - d) / (u - d)  # Risk-neutral probability

    # Initialize asset prices at maturity
    asset_prices = np.zeros(N + 1)
    asset_prices[0] = S * d**N
    for i in range(1, N + 1):
        asset_prices[i] = asset_prices[i-1] * (u/d)

    # Initialize option values at maturity
    option_values = np.zeros(N + 1)
    if option_type.lower() == 'call':
        option_values = np.maximum(asset_prices - K, 0)
    elif option_type.lower() == 'put':
        option_values = np.maximum(K - asset_prices, 0)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    # Backward induction
    for step in range(N-1, -1, -1):
        for i in range(step+1):
            # Expected option value
            option_values[i] = (p * option_values[i+1] + (1 - p) * option_values[i]) * np.exp(-r * dt)
            if american:
                # Calculate the asset price at this node
                asset_price = S * (u**i) * (d**(step - i))
                if option_type.lower() == 'call':
                    option_values[i] = max(option_values[i], asset_price - K)
                elif option_type.lower() == 'put':
                    option_values[i] = max(option_values[i], K - asset_price)

    return option_values[0]
