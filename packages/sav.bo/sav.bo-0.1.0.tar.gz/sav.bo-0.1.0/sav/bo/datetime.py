from datetime import date, timedelta
from typing import Iterator


def iterdates(start: date, stop: date = None, step: int = 1) -> Iterator[date]:
    """Yield dates from start until stop.

    The generated values include the start date but not the stop date.
    """
    while (stop is None) or (start < stop):
        yield start
        start = start + timedelta(step)


def isodate(s: str) -> date:
    """Convert ISO date string to date object."""
    return date(*[int(s[i:j]) for i, j in ((0, 4), (5, 7), (8, 10))])
