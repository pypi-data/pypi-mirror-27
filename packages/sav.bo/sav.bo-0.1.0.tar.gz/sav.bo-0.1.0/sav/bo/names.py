"""Convenience functions for working with names.

Names are strings that may be used as identifiers within programs
or as arguments in command-line interfaces. They typically do not
contain whitespace, commas or line breaks.
"""
from types import SimpleNamespace
from typing import Iterable, Tuple, Any, Union, Sequence, NamedTuple

from sav.bo.itertools import keymap


def split_names(names: Union[str, Iterable[str]]) -> Iterable[str]:
    """Split the specified argument into names.

    This method replicates the manner in which the
    :func:`collections.namedtuple` function parses its
    `field_names` argument. If `names` is a string, it
    is assumed to contain identifiers separated by
    commas and/or whitespace, and parsed accordingly.
    Otherwise, it is returned unaltered.
    """
    return (names.replace(',', ' ').split()
            if isinstance(names, str) else names)


def get_field_name(name: str) -> str:
    """Adjust to make a valid python field name.

    Replaces hyphens with underscores.

    :raise ValueError: if the result is not a valid identifier.
    """
    name = name.replace('-', '_')
    if not name.isidentifier():
        raise ValueError('Not an identifier: ' + name)
    if name.startswith('_'):
        raise ValueError('Name should not be private or magic: ' + name)
    return name


def ns_from_pairs(pairs: Iterable[Tuple[str, Any]]) -> Any:
    """Create namespace object from key-value pairs."""
    return SimpleNamespace(**dict(keymap(get_field_name, pairs)))


def ns_from_keys(keys: Union[str, Iterable[str]],
                 prefix='') -> Any:
    """Register characters or strings.

    This function returns a namespace object such that the
    name of every field matches the value of that field. It may
    therefore be used to group a collection of constant string
    values.

    :param keys: An iterable of strings. Note that this may also be
        a single string, in which case an attribute will be created
        for every character in the string.
    :param prefix: An optional prefix to be added to the field values.
    """
    return ns_from_pairs((key, prefix + key) for key in keys)


def ns_from_names(names: Union[str, Iterable[str]],
                  prefix: str= '') -> Any:
    """Register names.

    Similar to :func:`ns_from_keys`, except that this function will
    interpret a single string argument as a comma- and/or
    whitespace-separated list of names.

    :param names: Names to be split by :func:`split_names`.
    :param prefix: An optional prefix to be added to the field values.
    """
    return ns_from_keys(split_names(names), prefix)


def enum_names(names: Union[str, Iterable[str]],
               start: int=0) -> Any:
    pairs = map(reversed, enumerate(split_names(names), start))
    return ns_from_pairs(pairs)


