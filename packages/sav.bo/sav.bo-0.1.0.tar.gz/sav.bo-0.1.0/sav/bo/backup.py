"""Support for backup schemes."""
from datetime import date
from typing import (Set, Iterator, Callable, Iterable, Sized, AbstractSet)

from sav.bo.apriori import T


def hanoi_tresholds() -> Iterator[int]:
    """Tower of Hanoi style treshold generator function.

    To put an upper limit on the number of tresholds generated,
    simply wrap the call to this function in a call to
    :func:`bo.itertools.cap`.

    :return: A iterator which yields 0, 0b1, 0b11, 0b111, and so on.
    """
    power: int = 1
    while True:
        yield power - 1
        power <<= 1


def age_iter(ages: Iterable[int]) -> Iterator[int]:
    """Verify age values before passing them on.

    :param ages: If this iterable is :class:`Sized <collections.abc.Sized>`,
        then its elements will be returned in sorted order. If it is not,
        such as in the case of an iterator, then this function will verify
        that the ages are supplied in sorted order, raising an exception
        otherwise.

    :raise ValueError: If one of the following conditions obtains:

        -   the iterable is empty;
        -   a negative age value is encountered;
        -   the zero age value is missing;
        -   the supplied iterable is not
            :class:`Sized <collections.abc.Sized>` and does not yield
            the age values in the appropriate order;
        -   the same age value is received twice.

    :return: An iterator which yields age values from recent to older,
        starting with zero, and yielding each value only once.
    """

    # Sort if sized
    if isinstance(ages, Sized):
        # noinspection PyTypeChecker
        ages = sorted(ages)

    # First value should be zero
    ages = iter(ages)
    try:
        previous = next(ages)
        if previous:
            raise ValueError('Non-zero initial value ({})'.format(previous))
        yield previous
    except StopIteration:
        raise ValueError('No age values found.')

    # Subsequent values should be ascending
    for age in ages:
        if age <= previous:
            raise ValueError(
                'Age value {} is not older than {}'.format(age, previous)
            )
        previous = age
        yield age


def trim_ages(ages: Iterable[int],
              tresholds: Iterable[int] = None) -> Set[int]:
    """Trim a set of backups by age values.

    Determines which backups to keep on the basis of a number of
    treshold moments in time. For each treshold, the most recent backup
    will be kept that:

    1.  is at least as old as the treshold; and
    2.  was not already selected on the basis of a younger treshold.

    Note that if there is a time period at which less backups were made
    than the scheme allows this function to keep, condition (2) allows
    the function to keep more older backups instead.

    :param ages: Integer values representing backups by their age. The
        value for the most recent backup should be 0. It is up to the
        caller to decide what the unit of time should be.

    :param tresholds: Age treshold values. The function behaves a bit
        differently depending on the type of argument passed:

        -   If it is :class:`Sized <collections.abc.Sized>`, then its
            length determines the maximum amount of backups to be kept.
            The tresholds will be sorted before they are used in the
            algorithm, so the iterable may be a set or a sequence in
            any random ordering. One treshold should be zero.

        -   If it is an iterator, then it must yield the age tresholds
            from lower (more recent) to higher (older), because they
            will be consumed on the fly as the algorithm walks through
            the backups. This allows the use of an infinite iterator, in
            which case the maximum amount of backups becomes a function
            of the age of the oldest backup in the set. The first
            treshold should be zero.

        -   If it is `None` or left out, then a generator will be
            obtained from :func:`hanoi_tresholds`. This results in a
            Tower of Hanoi style rotation scheme.

    :return: The age values to be kept.

    """

    # Iterate over ages
    queue = age_iter(ages)

    # Ensure an appropriate iterable of tresholds
    if tresholds is None:
        tresholds = hanoi_tresholds()
    else:
        tresholds = age_iter(tresholds)

    # Fill a set of ages to keep and return them
    keep = set()
    for treshold in tresholds:
        for a in queue:
            if a >= treshold:
                keep.add(a)
                break
        else:
            break
    return keep


def trim(backups: AbstractSet[T], age: Callable[[T], int] = int,
         tresholds: Iterable[int] = None) -> Set[T]:
    """Trim a set of backups.

    Generic wrapper function around :func:`trim_ages` which accepts
    any set of backup objects.

    :param backups: Hashable objects representing individual archives.

    :param age: A function which returns the age of each archive,
        measured in the amount of backup periods that have elapsed
        since the most recent backup was made, where one backup period
        represents the minimal amount of time between two consecutive
        backups. The age value for the most recent backup should be 0.
        The default age function is `ìnt()`, which you can use if you
        either passed age values as backup objects directly, or if
        your backup objects have an ``__int__`` method that returns
        appropriate age values.

    :param tresholds: See :func:`trim_ages`.
    :return: The backups to be kept.

    """
    backup_map = {age(b): b for b in backups}
    keep = trim_ages(backup_map, tresholds)
    return {backup_map[a] for a in keep}


def trim_days(days: Set[date], tresholds: Iterable[int] = None) -> Set[date]:
    """Trim a set of daily backups.

    :param days: The dates to be trimmed.
    :param tresholds: See :func:`trim_ages`.
    :return: The dates to be kept.
    """
    current = max(days)

    def age(d: date):
        return (current - d).days

    return trim(days, age, tresholds)
