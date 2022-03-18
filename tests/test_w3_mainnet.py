import pytest
from bisect_scanner import EthereumScanner, PolygonScanner


POLYGON_ACCOUNT = "0x1C8e628381A7752C4bE1dd493427D4091e97ba7f"


@pytest.mark.skip()
def test_polygon():
    polygon = PolygonScanner()
    balance_history = [*polygon.balance_history(account=POLYGON_ACCOUNT)]
    assert balance_history == [
        (0, 0.0),
        (15556480, 712.275),
        (15591133, 562.275),
        (20856090, 462.274),
    ]


ETH_ACCOUNT = "0x790370ff5045bCeCc2161f0913302FCCC7Ee256d"


@pytest.mark.skip()
def test_ethereum():
    ethereum = EthereumScanner()
    balance_history = ethereum.balance_history(ETH_ACCOUNT)
    assert [*balance_history] == [(0, 0.0)]
    situation = [
        *ethereum.situation_scan(
            account=ETH_ACCOUNT,
            start_block=1100000,
            end_block=12485148,
            steps=30,
        )
    ]
    assert situation == [
        (11346608, 0.0),
        (11726112, 0.005),
        (11726112, 0.005),
        (12105616, 0.015),
        (12105616, 0.015),
        (12485120, 0.0),
    ]
    balance_history = [
        *ethereum.balance_history(
            account=ETH_ACCOUNT, end_block=12485148, situation_scan_steps=10
        )
    ]
