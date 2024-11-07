# American Options Calculator

A Python-based tool to calculate and visualize the pricing and Profit & Loss (P&L) of American stock options using the Binomial Options Pricing Model. The application features a user-friendly Streamlit interface for interactive trading assistance.

## Features

- **Binomial Options Pricing Model**: Calculate the fair price of American call and put options.
- **Profit & Loss Calculation**: Determine potential gains or losses based on your trading position.
- **Interactive Visualizations**: Plot P&L against varying underlying stock prices.
- **Real-Time Data Integration**: Fetch live stock and option data using APIs like `yfinance`.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/stock-options-calculator.git
   cd stock-options-calculator

2. **Create a Virtual Environment**

    ```bash
    Copy code
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Dependencies**

    ```bash
    Copy code
    pip install -r requirements.txt