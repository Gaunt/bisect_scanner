import operator as op
import pytest
from bisect_scanner.base_scanner import FakeChainScanner, SlowedDownScanner
from bisect_scanner.example_data import (
    BLOCK_BALANCES,
    BLOCK_BALANCES_2,
    BLOCK_BALANCES_LOW_ACTIVITY,
)


ACCOUNT = "account"


def test_block_balance():
    scanner = FakeChainScanner(BLOCK_BALANCES)
    assert scanner.block_balance(block=0, account=ACCOUNT) == 0
    assert scanner.block_balance(block=10, account=ACCOUNT) == 0
    assert scanner.block_balance(block=1000, account=ACCOUNT) == 0
    assert scanner.block_balance(block=1001, account=ACCOUNT) == 2000
    assert scanner.block_balance(block=2000, account=ACCOUNT) == 2000


def test_balance_history():
    scanner = FakeChainScanner(BLOCK_BALANCES)
    assert [
        *map(
            op.itemgetter(1),
            scanner.balance_history(end_block=1_000_001, account=ACCOUNT),
        )
    ] == [0, 2000, 1, 4000, 2, 10]
    assert [*map(tuple, scanner.balance_history(end_block=1_000_001, account=ACCOUNT))] == [
        (0, 0),
        (1001, 2000),
        (200_001, 1),
        (200_002, 4000),
        (200_101, 2),
        (1_000_001, 10),
    ]


def test_no_account():
    scanner = FakeChainScanner()
    with pytest.raises(ValueError):
        [*scanner.balance_history(account=None)]


def test_no_end_block():
    scanner = FakeChainScanner()
    balance_history = [*scanner.balance_history(account=ACCOUNT)]
    assert balance_history == [
        (0, 0),
        (1001, 2000),
        (200001, 1),
        (200002, 4000),
        (200101, 2),
    ]


def test_balance_history_with_interpolation():
    scanner = FakeChainScanner(
        BLOCK_BALANCES, interpolation_step=1
    )
    assert [*scanner.balance_history(end_block=1_000_001, account=ACCOUNT)] == [
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
    assert [*scanner.balance_history(end_block=2000, account=ACCOUNT)] == [
        (0, 0),
        (0, 0),
        (1, 1000),
        (5, 1001.5),
        (1000, 1003),
        (1001, 2000),
    ]


def test_balance_history_slowed_down():
    scanner = SlowedDownScanner(BLOCK_BALANCES)
    assert [
        *map(
            op.itemgetter(1),
            scanner.balance_history(account=ACCOUNT, end_block=1_000_001),
        )
    ] == [0, 2000, 1, 4000, 2, 10]
    assert [*map(tuple, scanner.balance_history(account=ACCOUNT, end_block=1_000_001))] == [
        (0, 0),
        (1001, 2000),
        (200_001, 1),
        (200_002, 4000),
        (200_101, 2),
        (1_000_001, 10),
    ]


def test_situation_scan():
    scanner = FakeChainScanner()
    assert [*scanner.situation_scan(account=ACCOUNT, steps=3)] == [
        (0, 0),
        (333333, 2),
    ]


def test_situation_scan_low_activity():
    scanner = FakeChainScanner(block_balances=BLOCK_BALANCES_LOW_ACTIVITY)
    end_block = scanner.last_block() * 2
    situation = [*scanner.situation_scan(account=ACCOUNT, steps=300, end_block=end_block)]
    assert situation == [(993383, 0), (1000050, 1000), (1006717, 0)]
    balances = [
        *scanner.balance_history(end_block=end_block, situation_scan_steps=300, account=ACCOUNT)
    ]
    assert balances == [(0, 0), (1000001, 1000), (1000101, 0)]
    balances = [*scanner.balance_history(end_block=end_block, account=ACCOUNT)]
    assert balances == [(0, 0), (1000001, 1000), (1000101, 0)]
