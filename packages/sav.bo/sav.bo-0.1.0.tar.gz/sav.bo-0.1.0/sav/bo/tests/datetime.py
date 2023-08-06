from datetime import date
from unittest import TestCase

from sav.bo.datetime import iterdates, isodate


class TestDateTime(TestCase):

    def test_iterdates(self):
        dates = set(iterdates(date(2016, 10, 14), date(2016, 11, 3)))
        k = '31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14'
        k = map(int, k.split())
        expected = {date(2016, 10, x) for x in k}
        expected |= {date(2016, 11, x) for x in (1, 2)}
        self.assertEqual(dates, expected)

    def test_isodate(self):
        self.assertEqual(isodate('2016-11-10'), date(2016, 11, 10))
        k = '1934-03-30'
        self.assertEqual(k, isodate(k).isoformat())
