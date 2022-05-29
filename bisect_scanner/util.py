import time
from typing import Iterable, Callable, TypeVar, List, Tuple
import operator as op
import itertools as it
import re


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


def slowed_down(
    balances: Iterable[Tuple[int, float]], delay: int = 1
) -> Iterable[Tuple[int, float]]:
    """
    testing purpose only
    """
    for balance in balances:
        time.sleep(delay)
        yield balance


def produce_gradual(
    balances: Iterable[Tuple[int, float]], end_block=None, delay=0
):
    balances_ = []
    for balance in slowed_down(balances, delay):
        balances_.append(balance)
        yield balances_.copy() + ([(end_block, 0)] if end_block else [])


def check_addr(address):
    if not isinstance(address, str):
        raise ValueError('address must be string')
    addr_regex = r'^(0x){1}[0-9a-fA-F]{40}$'
    return bool(re.match(addr_regex, address))
