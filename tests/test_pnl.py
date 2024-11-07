# tests/test_pnl.py

import unittest
from src.calculations.pnl import calculate_pnl

class TestPNL(unittest.TestCase):
    def test_long_position_profit(self):
        position = 'long'
        initial_premium = 10
        current_premium = 15
        quantity = 1
        pnl = calculate_pnl(position, initial_premium, current_premium, quantity)
        expected_pnl = 500  # (15 - 10) * 1 * 100
        self.assertEqual(pnl, expected_pnl)

    def test_long_position_loss(self):
        position = 'long'
        initial_premium = 10
        current_premium = 5
        quantity = 2
        pnl = calculate_pnl(position, initial_premium, current_premium, quantity)
        expected_pnl = (5 - 10) * 2 * 100  # -1000
        self.assertEqual(pnl, -1000)

    def test_short_position_profit(self):
        position = 'short'
        initial_premium = 12
        current_premium = 7
        quantity = 2
        pnl = calculate_pnl(position, initial_premium, current_premium, quantity)
        expected_pnl = (12 - 7) * 2 * 100  # 1000
        self.assertEqual(pnl, 1000)

    def test_short_position_loss(self):
        position = 'short'
        initial_premium = 12
        current_premium = 17
        quantity = 1
        pnl = calculate_pnl(position, initial_premium, current_premium, quantity)
        expected_pnl = (12 - 17) * 1 * 100  # -500
        self.assertEqual(pnl, -500)

    def test_invalid_position(self):
        position = 'invalid'
        initial_premium = 10
        current_premium = 15
        quantity = 1
        with self.assertRaises(ValueError):
            calculate_pnl(position, initial_premium, current_premium, quantity)

if __name__ == '__main__':
    unittest.main()
