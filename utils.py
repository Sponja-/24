from itertools import chain, combinations
from typing import Iterable, TypeVar

T = TypeVar("T")


def strict_powerset(iterable: Iterable[T]) -> chain[list[T]]:
    """Returns the powerset of s, excluding the empty set and s itself"""
    l = list(iterable)
    return chain.from_iterable(combinations(l, r) for r in range(1, len(l)))
