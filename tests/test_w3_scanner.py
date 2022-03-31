import pytest
from types import SimpleNamespace
from bisect_scanner import w3_scanner
from bisect_scanner import EtherScanner, PolygonScanner, FakeChainScanner
from unittest.mock import MagicMock

from web3 import (
    EthereumTesterProvider,
    Web3,
)


POLYGON_ACCOUNT = "0x1C8e628381A7752C4bE1dd493427D4091e97ba7f"
POLYGON_ACCOUNT_BALANCE_HISTORY = [
            (0, 0.0),
            (15556480, 712.275),
            (15591133, 562.275),
            (20856090, 462.274),
        ]


ETH_ACCOUNT = "0x790370ff5045bCeCc2161f0913302FCCC7Ee256d"
ETH_ACCOUNT_BALANCE_HISTORY = [
        (0, 0.0),
        (11503731, 0.005),
        (12103372, 0.015),
        (12107610, 0.009),
        (12425773, 0.0),
    ]


@pytest.fixture
def tester_provider():
    return EthereumTesterProvider()


@pytest.fixture
def eth_tester(tester_provider):
    return tester_provider.ethereum_tester


@pytest.fixture
def w3(tester_provider):
    return Web3(tester_provider)


@pytest.mark.skip()
def test_polygon():
    polygon = PolygonScanner()
    balance_history = [*polygon.balance_history(account=POLYGON_ACCOUNT, end_block=20856092)]
    assert balance_history == POLYGON_ACCOUNT_BALANCE_HISTORY


@pytest.mark.skip()
def test_ethereum():
    ether = EtherScanner()
    balance_history = [*ether.balance_history(ETH_ACCOUNT)]
    assert balance_history == ETH_ACCOUNT_BALANCE_HISTORY
