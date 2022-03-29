import pytest
from types import SimpleNamespace
from bisect_scanner import w3_scanner
from bisect_scanner import EtherScanner, PolygonScanner, FakeChainScanner
from unittest.mock import MagicMock


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


def fake_block_balance(account, block):
    if account == POLYGON_ACCOUNT:
        balance_history = POLYGON_ACCOUNT_BALANCE_HISTORY
    if account == ETH_ACCOUNT:
        balance_history = ETH_ACCOUNT_BALANCE_HISTORY
    balance = FakeChainScanner(balance_history).block_balance(block)
    return balance


class FakeWeb3:
    def __init__(self, provider, *args, **kwargs):
        self.eth = MagicMock()
        self.eth.getBalance = fake_block_balance
        if 'polygon' in provider.url:
            self.eth.blockNumber = 20856090 + 10
        else:
            self.eth.blockNumber = 12425773 + 10

    def isConnected(self):
        return True

    @staticmethod
    def WebsocketProvider(url):
        return SimpleNamespace(url=url)


# w3_scanner.web3.Web3 = FakeWeb3


@pytest.mark.skip()
def test_polygon():
    polygon = PolygonScanner()
    balance_history = [*polygon.balance_history(account=POLYGON_ACCOUNT, end_block=20856092)]
    assert balance_history == POLYGON_ACCOUNT_BALANCE_HISTORY


@pytest.mark.skip()
def test_ethereum():
    ether = EtherScanner()
    balance_history = [*ether.balance_history(ETH_ACCOUNT, end_block=12425779)]
    assert balance_history == ETH_ACCOUNT_BALANCE_HISTORY
