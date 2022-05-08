import pytest
from web3.providers import eth_tester
from bisect_scanner import EtherScanner, PolygonScanner
from eth_tester import EthereumTester #, MockBackend
from eth_account import Account, account
from web3 import EthereumTesterProvider, Web3

import eth_tester.backends.mock.main as mock_backend
from . import eth_mock_utils


mock_backend._get_default_account_data = eth_mock_utils.account_defaults
MockBackend = mock_backend.MockBackend


POLYGON_ACCOUNT = "0x1C8e628381A7752C4bE1dd493427D4091e97ba7f"
POLYGON_ACCOUNT_TEST_PRIV = (
    "0x171c24fb6ff126a7da63d361c7db60531e6b536ef7de06ae00ac229608efced7"
)
POLYGON_ACCOUNT_BALANCE_HISTORY = [
    (0, 0.0),
    (15556480, 712.275),
    (15591133, 562.275),
    (20856090, 462.274),
]

ETH_ACCOUNT = "0x98788F77e4b8519741d7E51B8F54f2F048Fcb5E0"
ETH_ACCOUNT_TEST_PRIV = (
    "0x0493aef9e36dca618f93e18e0bf849f8880524d98f0347084902bbd935c4732e"
)
ETH_ACCOUNT_BALANCE_HISTORY = [
    (0, 0.0),
    (11503731, 0.005),
    (12103372, 0.015),
    (12107610, 0.009),
    (12425773, 0.0),
]


SIMPLE_TRANSACTION = {
    "to": ETH_ACCOUNT,
    "gas_price": 0,
    "value": 0,
    "gas": 0,
}

@pytest.fixture
def tester_provider():
    ethereum_tester = EthereumTester(backend=MockBackend(alloc=()))
    return EthereumTesterProvider(ethereum_tester=ethereum_tester)


@pytest.fixture
def eth_tester_polygon(tester_provider):
    return tester_provider.ethereum_tester


@pytest.fixture
def w3(tester_provider):
    return Web3(tester_provider)


def insert_account(tester, w3, history=None):
    priv_key = ETH_ACCOUNT_TEST_PRIV
    tester.add_account(priv_key)
    account = w3.eth.account.from_key(priv_key)

    # for block, balance in ETH_ACCOUNT_BALANCE_HISTORY:
    #     tester.time_travel(block)
        
    print(tester.get_accounts()[-1])
    print(account.address)
    assert account.address == ETH_ACCOUNT


@pytest.fixture
def w3_with_eth_account(tester_provider):
    w3 = Web3(tester_provider)
    tester = tester_provider.ethereum_tester
    insert_account(tester, w3)
    return Web3(tester_provider)


@pytest.mark.skip()
def test_polygon_balance(w3_with_eth_account):
    polygon = PolygonScanner(w3=w3_with_eth_account, account=ETH_ACCOUNT)
    assert polygon.block_balance(ETH_ACCOUNT) == 0


@pytest.mark.skip()
def test_polygon_balance_history(w3_with_eth_account):
    polygon = PolygonScanner(w3=w3_with_eth_account)
    balance_history = [
        *polygon.balance_history(account=POLYGON_ACCOUNT, end_block=20856092)
    ]
    assert balance_history == POLYGON_ACCOUNT_BALANCE_HISTORY


@pytest.mark.skip()
def test_ethereum():
    ether = EtherScanner()
    balance_history = [*ether.balance_history(ETH_ACCOUNT)]
    assert balance_history == ETH_ACCOUNT_BALANCE_HISTORY


@pytest.mark.skip()
def test_polygon_mainnet():
    polygon = PolygonScanner()
    balance_history = [
        *polygon.balance_history(account=POLYGON_ACCOUNT, end_block=20856092)
    ]
    assert balance_history == POLYGON_ACCOUNT_BALANCE_HISTORY


@pytest.mark.skip()
def test_ethereum_mainnet():
    ether = EtherScanner()
    balance_history = [*ether.balance_history(ETH_ACCOUNT)]
    assert balance_history == ETH_ACCOUNT_BALANCE_HISTORY
