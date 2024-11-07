# tests/test_data_fetch.py

import unittest
from unittest.mock import patch
from src.data.data_fetch import get_real_time_price, get_option_chain

class TestDataFetch(unittest.TestCase):
    @patch('src.data.data_fetch.yf.Ticker')
    def test_get_real_time_price_success(self, mock_ticker):
        # Mock the Ticker object and its history method
        mock_history = mock_ticker.return_value.history
        mock_history.return_value = {'Close': [150.0]}
        
        price = get_real_time_price('AAPL')
        self.assertEqual(price, 150.0)

    @patch('src.data.data_fetch.yf.Ticker')
    def test_get_real_time_price_failure(self, mock_ticker):
        # Simulate an exception during data fetching
        mock_history = mock_ticker.return_value.history
        mock_history.side_effect = Exception("API Error")
        
        price = get_real_time_price('INVALID')
        self.assertIsNone(price)

    @patch('src.data.data_fetch.yf.Ticker')
    def test_get_option_chain_success(self, mock_ticker):
        # Mock the Ticker object and its option_chain method
        mock_option_chain = mock_ticker.return_value.option_chain
        mock_option_chain.return_value = type('obj', (object,), {'calls': 'calls_data', 'puts': 'puts_data'})
        
        calls, puts = get_option_chain('AAPL', '2024-12-20')
        self.assertEqual(calls, 'calls_data')
        self.assertEqual(puts, 'puts_data')

    @patch('src.data.data_fetch.yf.Ticker')
    def test_get_option_chain_failure(self, mock_ticker):
        # Simulate an exception during option chain fetching
        mock_option_chain = mock_ticker.return_value.option_chain
        mock_option_chain.side_effect = Exception("API Error")
        
        calls, puts = get_option_chain('AAPL', '2024-12-20')
        self.assertIsNone(calls)
        self.assertIsNone(puts)

if __name__ == '__main__':
    unittest.main()
