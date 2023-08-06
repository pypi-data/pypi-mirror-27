"""Tools that further extend the standard :mod:`itertools` library module."""
import collections
from itertools import chain
from typing import (TypeVar, Iterable, Iterator, Callable, Tuple, Optional,
                    Container, Union, AbstractSet, Dict)

from sav.bo.apriori import T

KT = TypeVar('KT')  # Key type.
KT_A = TypeVar('KT_A')  # Key type.
KT_B = TypeVar('KT_B')  # Key type.

VT = TypeVar('VT')  # Value type.
VT_A = TypeVar('VT_A')  # Value type.
VT_B = TypeVar('VT_B')  # Value type.

somevar = 3  #: Sample doc comment for somevar


def any_iter(elements: Iterable[T]) -> Optional[Iterator[T]]:
    """Check whether an iterable will yield any elements.

    This method pre-fetches the first element, and reconstructs
    an iterator including that element unless no first element was
    encountered.

    :param elements: Any iterable object.
    :return: `None` if the specified iterable yields no elements.
        Otherwise an iterator over the specified iterable is returned.
    """
    iterator = iter(elements)
    try:
        e = next(iterator)
    except StopIteration:
        return None
    else:
        return chain([e], iterator)


def unique(elements: Iterable[T]) -> Iterator[T]:
    """Iterates over each element only once.

    Iterating over ``unique(elements)`` is similar to iterating over
    ``set(elements)``, except for the following differences:

    -   It preserves the order of elements.
    -   It passes each element through before reading the next element.

    These differences matter to loops with conditional breaks::

        for e in unique(elements):
            foo(e)
            if bar(e):
                break

    Note that this code runs without problems if ``elements`` happens to
    be an infinite iterator like `itertools.count`. By contrast, the
    expression ``set(itertools.count())`` will keep eating memory without
    terminating.

    The differences also matter if ``elements`` happens to be a large
    finite iterable. Suppose it is a sequence of 10.000 elements,
    while the ``bar`` condition is satisfied by its 5th element. Then the
    example code will only iterate 5 times. By contrast, iterating over
    ``set(elements)`` would require 10.000 iterations over the sequence
    just to fill the set. Furthermore, the subsequent number of calls to
    ``foo`` would be an undetermined amount between 1 and the length of
    the set.

    :param elements: An iterable of `hashable` elements.
    :return: An iterator returning each element only once.
    """
    seen = set()
    for e in elements:
        if e not in seen:
            seen.add(e)
            yield e


def skip(exclude: Union[Container[T], Iterable[T]],
         source: Iterable[T]) -> Iterator[T]:
    """Iterates over elements from `source` not in `exclude`.

    :param exclude: The elements to be skipped.
    :param source: The elements to be iterated over.
    :return: An iterator object.

    If ``exclude`` is a set or set-like object, or if it is a
    container but not an iterable, then its ``__contains__`` method
    will be used to determine which objects must be skipped.

    Otherwise, ``exclude`` will be iterated over precisely once, so it
    is safe to pass generators or input streams. What happens next
    depends on whether this yields hashable elements:

    -   If all elements of ``exclude`` are hashable, then they are
        placed in a :class:`set` which will be used to determine
        whether elements from ``source`` must be skipped.

    -   If one or more elements of ``exclude`` are not hashable, and
        ``exclude`` is also a container, then we fall back on its
        ``__contains__`` method to determine which objects must be
        skipped.

    -   Finally, if ``exclude`` is not a container and neither are all
        its elements hashable, then they are placed in a tuple instead.
        Keep in mind that looking up each element from ``source`` in this
        tuple will lead to quadratic time complexity based on the lengths
        of ``exclude`` and ``source``.

    """
    if isinstance(exclude, Iterable) and not isinstance(exclude, AbstractSet):
        collected = tuple(exclude)
        try:
            exclude = set(collected)
        except TypeError:
            if not isinstance(exclude, Container):
                exclude = collected
    return filter(lambda e: e not in exclude, source)


def skip_none(elements: Iterable[Optional[T]]) -> Iterator[T]:
    """Iterates over all elements that are not `None`.

    Aside from being a conventient shorthand, this function makes
    it easier for type checkers to convert an optional type into
    a type that rules out `None`.
    """
    return filter(lambda e: e is not None, elements)


def cap(iterable: Iterable[T], max_len: int) -> Iterator[T]:
    """Iterates over a maximum number of elements."""
    iterator = iter(iterable)
    for i in range(max_len):
        try:
            yield next(iterator)
        except StopIteration:
            break


def nth(iterable: Iterable[Tuple], index: int) -> Iterator:
    """Yields the nth element of each tuple."""
    return (tup[index] for tup in iterable)


def first(iterable: Iterable[Tuple]) -> Iterator:
    """Yields the first element of each tuple."""
    return nth(iterable, 0)


def last(iterable: Iterable[Tuple]) -> Iterator:
    """Yields the last element of each tuple."""
    return nth(iterable, -1)


def starfilter(func: Callable[..., bool],
               iterable: Iterable[Tuple]) -> Iterator[Tuple]:
    """Starred companion to the `filter` builtin."""
    return (tup for tup in iterable if func(*tup))


def keymap(func: Callable[[KT_A], KT_B],
           iterable: Iterable[Tuple[KT_A, VT]]) -> Iterator[Tuple[KT_B, VT]]:
    """Apply a function to the keys of key-value pairs."""
    return ((func(k), v) for k, v in iterable)


def valmap(func: Callable[[VT_A], VT_B],
           iterable: Iterable[Tuple[KT, VT_A]]) -> Iterator[Tuple[KT, VT_B]]:
    """Apply a function to the values of key-value pairs."""
    return ((k, func(v)) for k, v in iterable)


def keyfilter(func: Callable[[KT], bool],
              iterable: Iterable[Tuple[KT, VT]]) -> Iterator[Tuple[KT, VT]]:
    return ((k, v) for k, v in iterable if func(k))


def valfilter(func: Callable[[VT], bool],
              iterable: Iterable[Tuple[KT, VT]]) -> Iterator[Tuple[KT, VT]]:
    return ((k, v) for k, v in iterable if func(v))


def iterarg(opt: Optional[Iterable[T]]) -> Iterable[T]:
    """Turn optional iterables into iterables.

    :return: An empty tuple if the argument is `None`, otherwise the argument
        is passed through.
    """
    return () if opt is None else opt


class ClusterBufferError(Exception):
    def __init__(self):
        super().__init__('Maximum buffer size reached.')


def clustered(func: Callable[[VT], KT], iterable: Iterable[VT],
              buffer_max: int = 0) -> Iterator[Tuple[KT, Iterator[VT]]]:
    """Divides objects into different clusters."""

    key_buffer = collections.deque()
    val_buffers: Dict[KT, collections.deque] = {}
    buffer_size = 0

    # Generate key-value pairs and maintain buffers
    def source_generator() -> Iterator[Tuple[KT, VT]]:
        for val in iterable:
            key = func(val)
            if key not in val_buffers:
                val_buffers[key] = collections.deque()
                key_buffer.append(key)
            yield key, val

    source_iter = source_generator()

    # Read from the specified buffer
    def buffered_generator(buffer: collections.deque) -> Iterator:
        nonlocal buffer_size
        while True:
            try:
                val = buffer.popleft()
            except IndexError:
                try:
                    key, val = next(source_iter)
                except StopIteration:
                    return
                val_buffers[key].append(val)
                if buffer_max:
                    buffer_size += 1
                    if buffer_size == buffer_max:
                        raise ClusterBufferError()
            else:
                if buffer_max:
                    buffer_size -= 1
                yield val

    # Generate values for the specified key
    def sub_generator(key: KT) -> Iterator[VT]:
        yield from buffered_generator(val_buffers[key])

    # Generate a sub iterator for each new key in the key buffer
    for k in buffered_generator(key_buffer):
        yield k, sub_generator(k)
