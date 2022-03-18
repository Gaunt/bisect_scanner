import operator as op
from bisect_scanner.base_scanner import FakeChainScanner
from bisect_scanner.example_data import (
    BLOCK_BALANCES,
    BLOCK_BALANCES_2,
    BLOCK_BALANCES_LOW_ACTIVITY,
)


ACCOUNT = "account"


def test_block_balance():
    scanner = FakeChainScanner(BLOCK_BALANCES, account=ACCOUNT)
    assert scanner.block_balance(0) == 0
    assert scanner.block_balance(10) == 0
    assert scanner.block_balance(1000) == 0
    assert scanner.block_balance(1001) == 2000
    assert scanner.block_balance(2000) == 2000


def test_balance_history():
    scanner = FakeChainScanner(BLOCK_BALANCES, account=ACCOUNT)
    assert [
        *map(
            op.itemgetter(1),
            scanner.balance_history(end_block=1_000_001),
        )
    ] == [0, 2000, 1, 4000, 2, 10]
    assert [*map(tuple, scanner.balance_history(end_block=1_000_001))] == [
        (0, 0),
        (1001, 2000),
        (200_001, 1),
        (200_002, 4000),
        (200_101, 2),
        (1_000_001, 10),
    ]


def test_balance_history_with_interpolation():
    scanner = FakeChainScanner(
        BLOCK_BALANCES, interpolation_step=1, account=ACCOUNT
    )
    assert [*scanner.balance_history(end_block=1_000_001)] == [
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
    scanner = FakeChainScanner(
        BLOCK_BALANCES_2, interpolation_step=4, account=ACCOUNT
    )
    assert [*scanner.balance_history(end_block=2000)] == [
        (0, 0),
        (0, 0),
        (1, 1000),
        (5, 1001.5),
        (1000, 1003),
        (1001, 2000),
    ]


def test_situation_scan():
    scanner = FakeChainScanner()
    assert [*scanner.situation_scan(steps=3)] == [
        (0, 0),
        (333333, 2),
    ]


def test_situation_scan_low_activity():
    scanner = FakeChainScanner(block_balances=BLOCK_BALANCES_LOW_ACTIVITY)
    end_block = scanner.last_block() * 2
    situation = [*scanner.situation_scan(steps=300, end_block=end_block)]
    assert situation == [(993383, 0), (1000050, 1000), (1006717, 0)]
    balances = [
        *scanner.balance_history(end_block=end_block, situation_scan_steps=300)
    ]
    assert balances == [(0, 0), (1000001, 1000), (1000101, 0)]
    balances = [*scanner.balance_history(end_block=end_block)]
    assert balances == [(0, 0), (1000001, 1000), (1000101, 0)]
