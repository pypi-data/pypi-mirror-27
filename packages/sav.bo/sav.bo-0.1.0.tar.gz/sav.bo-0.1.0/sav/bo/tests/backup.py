from datetime import date
from unittest import TestCase

from sav.bo.datetime import iterdates, isodate
from sav.bo.backup import trim, trim_days


class TestBackup(TestCase):

    def test_hanoi_tresholds(self):

        # Suppose we still have all backups from 20 days
        sample = set(range(20))

        # Then we expect to keep just the treshold values
        expected = {0, 1, 3, 7, 15}
        result = trim(sample)
        self.assertEqual(result, expected)

        # Lets add a backup one day later
        sample = {x + 1 for x in expected}
        sample.add(0)
        self.assertEqual(sample, {0, 1, 2, 4, 8, 16})

        # Now we expect the two day old backup to be dropped
        expected = sample - {2}
        result = trim(sample)
        self.assertEqual(result, expected)

        # Lets make it two days later and suppose that the
        # backup script did not run on the first of those two days
        sample = {x + 2 for x in expected}
        sample.add(0)
        self.assertEqual(sample, {0, 2, 3, 6, 10, 18})

        # Because we only made one new backup, we still only drop one
        expected = sample - {6}
        result = trim(sample)
        self.assertEqual(result, expected)

    # TODO: add more tests
    def test_trim_days(self):

        # First test: if we had all dates
        # Consider the following timeline:
        # 02 01 31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14
        dates = set(iterdates(date(2016, 10, 14), date(2016, 11, 3)))

        # This should translate into the following age values:
        #  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
        # The Hanoi scheme retains the following ages:
        #  0  1     3           7                      15
        # Hence the follow dates should be kept:
        # 02 01    30          26                      18
        trimmed = trim_days(dates)
        expected = set(map(isodate,
                           ('2016-10-18', '2016-10-26', '2016-10-30',
                            '2016-11-01', '2016-11-02')
                           ))
        self.assertEqual(trimmed, expected)
