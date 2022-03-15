import time
import os
from functools import lru_cache
from typing import Union
from web3 import Web3
from dotenv import load_dotenv
from bisect_scanner.base_scanner import BaseScanner

load_dotenv()


URL = os.environ('URL', '')
DECIMALS = 18
DELAY = 0.0


class PolygonScanner(BaseScanner):

    def __init__(self, account, w3: Union[str, Web3] = URL, *args, **kwargs):
        if isinstance(w3, str):
            self.web3 = Web3(Web3.WebsocketProvider(w3))
        else:
            self.web3 = w3
        self.account = account
        super().__init__(*args, **kwargs)

    @lru_cache(10000)
    def block_balance(self, block):
        time.sleep(DELAY)
        balance = round(
            self.w3().eth.getBalance(str(self.account), block) * pow(10, -DECIMALS),
            self.precission,
        )
        return round(balance, self.precission)

    def last_block(self):
        return self.w3().eth.blockNumber

    def w3(self):
        return self.web3
