# tests/test_binomial_model.py

import unittest
from src.pricing.binomial_model import binomial_option_price

class TestBinomialModel(unittest.TestCase):
    def test_call_option_price(self):
        S = 100
        K = 100
        T = 1
        r = 0.05
        sigma = 0.2
        option_type = 'call'
        american = True
        N = 100
        price = binomial_option_price(S, K, T, r, sigma, option_type, american, N)
        expected_price = 10.45  # Example expected value; adjust based on actual calculations
        self.assertAlmostEqual(price, expected_price, places=1)

    def test_put_option_price(self):
        S = 100
        K = 100
        T = 1
        r = 0.05
        sigma = 0.2
        option_type = 'put'
        american = True
        N = 100
        price = binomial_option_price(S, K, T, r, sigma, option_type, american, N)
        expected_price = 5.57  # Example expected value; adjust based on actual calculations
        self.assertAlmostEqual(price, expected_price, places=1)

    def test_invalid_option_type(self):
        S = 100
        K = 100
        T = 1
        r = 0.05
        sigma = 0.2
        option_type = 'invalid'
        american = True
        N = 100
        with self.assertRaises(ValueError):
            binomial_option_price(S, K, T, r, sigma, option_type, american, N)

if __name__ == '__main__':
    unittest.main()
