import unittest

from anji_orm.syntax.query import Interval


class IntervalTest(unittest.TestCase):

    def test_interval_contains(self):
        self.assertTrue(5 in Interval(4, 6))
        self.assertTrue(5 in Interval(4, 5, right_close=True))
        self.assertTrue(5 in Interval(5, 6, left_close=True))
        self.assertTrue(5 not in Interval(4, 5))
        self.assertTrue(5 not in Interval(7, 8))

    def test_internal_contains_interval(self):
        self.assertTrue(Interval(3, 7).contains_interval(Interval(4, 6)))
        self.assertTrue(Interval(4, 7).contains_interval(Interval(4, 6)))
        self.assertTrue(Interval(3, 6).contains_interval(Interval(4, 6)))

        self.assertFalse(Interval(4, 6).contains_interval(Interval(3, 7)))
        self.assertFalse(Interval(4, 6).contains_interval(Interval(4, 7)))
        self.assertFalse(Interval(4, 6).contains_interval(Interval(3, 6)))

        self.assertTrue(Interval(4, 7, left_close=True).contains_interval(Interval(4, 6)))
        self.assertFalse(Interval(4, 7).contains_interval(Interval(4, 6, left_close=True)))
        self.assertTrue(Interval(4, 7, right_close=True).contains_interval(Interval(5, 7)))
        self.assertFalse(Interval(4, 7).contains_interval(Interval(5, 7, right_close=True)))
