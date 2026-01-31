import unittest

from pymcdm.distances import draWS, kemeny, frobenius


class TestDistancesDraWS(unittest.TestCase):
    """
    Test drastic WS distance implementation.

    Based on: Sałabun, W., & Shekhovtsov, A. (2023, September). An innovative drastic metric for ranking
    similarity in decision-making problems. In 2023 18th Conference on Computer Science and Intelligence
    Systems (FedCSIS) (pp. 731-738). IEEE.
    """

    def test_draws_raises_on_empty(self):
        with self.assertRaises(ValueError):
            draWS([], [1, 2, 3])
        with self.assertRaises(ValueError):
            draWS([1, 2, 3], [])

    def test_draws(self):
        cases = [
            ((1, 2, 3, 4, 5), 0.0),
            ((2, 1, 3, 4, 5), 0.7742),
            ((1, 3, 2, 4, 5), 0.3871),
            ((1, 2, 4, 3, 5), 0.1935),
            ((1, 2, 3, 5, 4), 0.0968),
            ((3, 2, 1, 4, 5), 0.6452),
            ((4, 2, 3, 1, 5), 0.5806),
            ((5, 2, 3, 4, 1), 0.5484),
        ]
        for r, ev in cases:
            with self.subTest(r=r, expected_value=ev):
                self.assertAlmostEqual(draWS((1, 2, 3, 4, 5), r), ev, places=4)


class TestDistancesKemeny(unittest.TestCase):
    """
    Test Kemeny distance implementation.

    Based on: Kemeny, J. G. (1959). Mathematics without numbers. Daedalus, 88(4), 577-591.
    """
    def test_kemeny_raises_on_empty(self):
        with self.assertRaises(ValueError):
            kemeny([], [1, 2, 3])
        with self.assertRaises(ValueError):
            kemeny([1, 2, 3], [])

    def test_kemeny(self):
        cases = [
            ((1, 2, 3), 0.0),
            ((1, 2.5, 2.5), 1.0),
            ((1, 3, 2), 2.0),
            ((1.5, 3, 1.5), 3.0),
            ((2, 3, 1), 4.0),
            ((2.5, 2.5, 1), 5.0),
            ((3, 2, 1), 6.0),
            ((3, 1.5, 1.5), 5.0),
            ((3, 1, 2), 4.0),
            ((2.5, 1, 2.5), 3.0),
            ((2, 1, 3), 2.0),
            ((1.5, 1.5, 3), 1.0),
            ((2, 2, 2), 3.0)
        ]
        for r, ev in cases:
            with self.subTest(r=r, expected_value=ev):
                self.assertAlmostEqual(kemeny((1, 2, 3), r), ev)


class TestDistancesFrobenius(unittest.TestCase):
    """
    Test Frobenius distance implementation.

    Based on: Dezert, J., Shekhovtsov, A., & Sałabun, W. (2024).
    A new distance between rankings. Heliyon, 10(7).
    """
    def test_frobenius_raises_on_empty(self):
        with self.assertRaises(ValueError):
            frobenius([], [1, 2, 3])
        with self.assertRaises(ValueError):
            frobenius([1, 2, 3], [])

    def test_frobenius(self):
        cases = [
            ((1, 2, 3), 0.0000),
            ((1, 2.5, 2.5), 1.4142),
            ((1, 3, 2), 2.8284),
            ((1.5, 3, 1.5), 3.1623),
            ((2, 3, 1), 4.0000),
            ((2.5, 2.5, 1), 4.2426),
            ((3, 2, 1), 4.8990),
            ((3, 1.5, 1.5), 4.2426),
            ((3, 1, 2), 4.0000),
            ((2.5, 1, 2.5), 3.1623),
            ((2, 1, 3), 2.8284),
            ((1.5, 1.5, 3), 1.4142),
            ((2, 2, 2), 2.4495)
        ]
        for r, ev in cases:
            with self.subTest(r=r, expected_value=ev):
                self.assertAlmostEqual(frobenius((1, 2, 3), r), ev, places=4)
