import unittest

from big_integer_nth_root import nth_root, floor_nth_root
from big_integer_nth_root.core import _initial_guess


class TestBasic(unittest.TestCase):

    def test_alias_is_same_callable(self):
        self.assertIs(floor_nth_root, nth_root)

    def test_zero(self):
        self.assertEqual(nth_root(0, 2), 0)
        self.assertEqual(nth_root(0, 7), 0)

    def test_one(self):
        self.assertEqual(nth_root(1, 1), 1)
        self.assertEqual(nth_root(1, 100), 1)

    def test_k_one_returns_input(self):
        self.assertEqual(nth_root(123456789, 1), 123456789)
        self.assertEqual(nth_root(0, 1), 0)

    def test_perfect_squares(self):
        self.assertEqual(nth_root(9, 2), 3)
        self.assertEqual(nth_root(10000, 2), 100)
        self.assertEqual(nth_root(1 << 40, 2), 1 << 20)

    def test_perfect_cubes(self):
        self.assertEqual(nth_root(27, 3), 3)
        self.assertEqual(nth_root(1000, 3), 10)
        self.assertEqual(nth_root(1 << 60, 3), 1 << 20)

    def test_perfect_high_powers(self):
        self.assertEqual(nth_root(1 << 100, 10), 1 << 10)
        self.assertEqual(nth_root(1 << 1000, 100), 1 << 10)

    def test_non_perfect_floor(self):
        # 10 is between 3**2=9 and 4**2=16.
        self.assertEqual(nth_root(10, 2), 3)
        # 124 is between 5**3=125? no, 4**3=64 and 5**3=125, so floor is 4.
        self.assertEqual(nth_root(124, 3), 4)
        self.assertEqual(nth_root(125, 3), 5)
        self.assertEqual(nth_root(126, 3), 5)

    def test_just_below_perfect_power(self):
        self.assertEqual(nth_root((1 << 100) - 1, 10), (1 << 10) - 1)


class TestLarge(unittest.TestCase):

    def test_huge_exact_root(self):
        base = 123456789012345678901234567890
        for k in (2, 3, 5, 17):
            n = base ** k
            self.assertEqual(nth_root(n, k), base)

    def test_huge_plus_one(self):
        base = 123456789012345678901234567890
        for k in (2, 3, 5, 17):
            self.assertEqual(nth_root(base ** k + 1, k), base)

    def test_huge_minus_one(self):
        base = 123456789012345678901234567890
        for k in (2, 3, 5, 17):
            self.assertEqual(nth_root(base ** k - 1, k), base - 1)

    def test_thousand_digit_number(self):
        # A number with ~1000 decimal digits and a known 5th root.
        base = 10 ** 200
        n = base ** 5
        self.assertEqual(nth_root(n, 5), base)
        self.assertEqual(nth_root(n - 1, 5), base - 1)

    def test_initial_guess_upper_bound_for_big_input(self):
        # For big inputs the guess is a bit-length upper bound; it must be
        # >= the true root so Newton converges from above.
        n = (1 << 60) - 1
        k = 3
        root = nth_root(n, k)
        guess = _initial_guess(n, k)
        self.assertGreaterEqual(guess, root)


class TestErrors(unittest.TestCase):

    def test_negative_n(self):
        with self.assertRaises(ValueError):
            nth_root(-1, 2)

    def test_k_zero(self):
        with self.assertRaises(ValueError):
            nth_root(5, 0)

    def test_k_negative(self):
        with self.assertRaises(ValueError):
            nth_root(5, -2)

    def test_n_not_int(self):
        with self.assertRaises(TypeError):
            nth_root(3.0, 2)
        with self.assertRaises(TypeError):
            nth_root("16", 2)

    def test_k_not_int(self):
        with self.assertRaises(TypeError):
            nth_root(16, 2.0)
        with self.assertRaises(TypeError):
            nth_root(16, "2")

    def test_bool_rejected(self):
        # bool is a subclass of int; we treat it as a type error to avoid
        # surprising silent coercion (e.g. k=True meaning k==1).
        with self.assertRaises(TypeError):
            nth_root(16, True)
        with self.assertRaises(TypeError):
            nth_root(True, 2)


if __name__ == "__main__":
    unittest.main()
