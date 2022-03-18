from typing import Iterable, Callable, TypeVar, List
import operator as op
import itertools as it


def scan_steps(start_block: int, end_block: int, steps: int) -> List[int]:
    """
    >>> scan_steps(0, 10, 5)
    [0, 2, 4, 6, 8, 10]
    >>> scan_steps(5, 11, 3)
    [5, 7, 9, 11]
    """
    diff = end_block - start_block
    return [start_block + step * (diff // steps) for step in range(steps + 1)]


T = TypeVar("T")


def uniq(iterable: Iterable[T], fun: Callable[[T, T], bool] = op.eq):
    """
    >>> [*uniq([1,1,4,1,1])]
    [1, 4, 1]
    >>> [*uniq([1,4,4,1])]
    [1, 4, 1]
    >>> [*uniq([1,4])]
    [1, 4]
    >>> [*uniq([1])]
    [1]
    """
    iterable = iter(iterable)
    prev = next(iterable)
    yield prev
    for v in iterable:
        if not fun(prev, v):
            yield v
            prev = v
