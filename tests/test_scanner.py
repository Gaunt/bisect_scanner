import operator as op
from bisect_scanner.base_scanner import FakeChainScanner


BLOCK_BALANCES = [
    (0, 0),
    (1000, 2000),
    (200_000, 1),
    (200_001, 4000),
    (200_100, 2),
    (1_000_000, 10),
]


BLOCK_BALANCES_2 = [
    (0, 1000),
    (1, 1000),
    (2, 1000),
    (3, 1003),
    (1000, 2000),
]


def test_block_balance():
    scanner = FakeChainScanner(BLOCK_BALANCES)
    assert scanner.block_balance(0) == 0
    assert scanner.block_balance(10) == 0
    assert scanner.block_balance(1000) == 0
    assert scanner.block_balance(1001) == 2000
    assert scanner.block_balance(2000) == 2000


def test_balance_history():
    scanner = FakeChainScanner(BLOCK_BALANCES)
    assert [
        *map(
            op.itemgetter(1),
            scanner.balance_history(0, 1_000_001),
        )
    ] == [0, 2000, 1, 4000, 2, 10]
    assert [*map(tuple, scanner.balance_history(0, 1_000_001))] == [
        (0, 0),
        (1001, 2000),
        (200_001, 1),
        (200_002, 4000),
        (200_101, 2),
        (1_000_001, 10),
    ]


def test_balance_history_with_interpolation():
    scanner = FakeChainScanner(BLOCK_BALANCES, interpolation_step=1)
    assert [
        *scanner.balance_history(0, 1_000_001)
    ] == [
        (0, 0),
        (1000, 0),
        (1001, 2000),
        (200000, 2000),
        (200001, 1),
        (200001, 1),
        (200002, 4000),
        (200100, 4000),
        (200101, 2),
        (1000000, 2),
        (1000001, 10),
    ]
    scanner = FakeChainScanner(BLOCK_BALANCES_2, interpolation_step=4)
    assert [*scanner.balance_history(0, 2000)] == [
        (0, 0),
        (0, 0),
        (1, 1000),
        (5, 1001.5),
        (1000, 1003),
        (1001, 2000),
    ]
