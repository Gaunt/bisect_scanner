import time
import os
from pathlib import Path
from functools import lru_cache
from typing import Union
from web3 import Web3
from dotenv import load_dotenv
from bisect_scanner.base_scanner import BaseScanner


user_config = Path(os.path.expanduser("~")) / '.config/bisect_scanner_rc'


if user_config.exists():
    load_dotenv(user_config)


W3_URL = os.getenv("W3_URL", "")
DECIMALS = 18
DELAY = 0.0
CACHE_SIZE = 10000


class W3Scanner(BaseScanner):
    def __init__(
        self, account=None, w3: Union[str, Web3] = W3_URL, *args, **kwargs
    ):
        if isinstance(w3, str):
            self.web3 = Web3(Web3.WebsocketProvider(w3))
        else:
            self.web3 = w3

        if not self.web3.isConnected():
            raise ValueError("w3 not connected")

        self.account = account
        super().__init__(*args, **kwargs)

    @lru_cache(CACHE_SIZE)
    def block_balance(self, block):
        time.sleep(DELAY)
        balance = round(
            self.w3().eth.getBalance(str(self.account), block)
            * pow(10, -DECIMALS),
            self.precission,
        )
        return round(balance, self.precission)

    def last_block(self):
        return self.w3().eth.blockNumber

    def w3(self):
        return self.web3


def EthereumScanner():
    ETHEREUM_URL = os.getenv("ETHEREUM_URL", "")
    return W3Scanner(w3=ETHEREUM_URL)


def PolygonScanner():
    POLYGON_URL = os.getenv("POLYGON_URL", "")
    return W3Scanner(w3=POLYGON_URL)
