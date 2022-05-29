import time
import json
import os
from pathlib import Path
from functools import lru_cache
from typing import Union
import web3
from bisect_scanner.base_scanner import BaseScanner
from bisect_scanner.config import config
import requests


W3_URL = os.getenv("W3_URL", "")
DECIMALS = 18
DELAY = 0.0
CACHE_SIZE = 100_000


ABI = """[
  {
    "constant": true,
    "inputs": [
      {
        "name": "account",
        "type": "address"
      }
    ],
    "name": "balanceOf",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "decimals",
    "outputs": [
      {
        "name": "",
        "type": "uint8"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  }
]"""

ABI = json.loads(ABI)


def get_contract_balance(w3, contract_address, account, block):
    contract_address = web3.Web3.toChecksumAddress(contract_address)
    contract = w3.eth.contract(address=contract_address, abi=ABI)
    return contract.functions.balanceOf(account).call(block_identifier=block)


def get_contract_decimals(w3, contract_address):
    contract_address = web3.Web3.toChecksumAddress(contract_address)
    contract = w3.eth.contract(address=contract_address, abi=ABI)
    return contract.functions.decimals().call()


class W3Scanner(BaseScanner):
    def __init__(
        self,
        w3: Union[str, web3.Web3] = W3_URL,
        contract_address=None,
        *args,
        **kwargs,
    ):
        if isinstance(w3, str):
            self.web3 = web3.Web3(web3.Web3.WebsocketProvider(w3))
        else:
            self.web3 = w3

        if not self.web3.isConnected():
            raise ValueError("w3 not connected")
        self.contract_address = contract_address
        if contract_address:
            self.decimals = get_contract_decimals(self.web3, contract_address)
        else:
            self.decimals = DECIMALS
        super().__init__(*args, **kwargs)

    @lru_cache(CACHE_SIZE)
    def block_balance(self, account, block=None):
        time.sleep(DELAY)
        if not block:
            block = self.last_block()
        if self.contract_address:
            balance = self.token_balance(
                account, block, self.contract_address
            )
        else:
            balance = self.w3().eth.getBalance(str(self.account), block)
        if balance is None:
            return None
        else:
            return round(balance * pow(10, -self.decimals), self.precission)

    def token_balance(self, account, block, contract_address):
        try:
            return get_contract_balance(
                self.web3, contract_address, account, block
            )
        except web3.exceptions.BadFunctionCallOutput:
            return None

    def last_block(self):
        return self.w3().eth.blockNumber

    def w3(self):
        return self.web3


def check_config(wr_url, **kwargs):
    pass


class EtherScanner(W3Scanner):
    def __init__(self, *args, **kwargs):
        super().__init__(w3=config.ETHEREUM_URL, *args, **kwargs)


class PolygonScanner(W3Scanner):
    def __init__(self, *args, **kwargs):
        kwargs = {'w3': config.POLYGON_URL, **kwargs}
        super().__init__(*args, **kwargs)


class EthereumERC20Scanner(W3Scanner):
    def __init__(self, contract_address, *args, **kwargs):
        super().__init__(
            w3=config.ETHEREUM_URL, contract_address=contract_address, *args, **kwargs
        )


class PolygonERC20Scanner(W3Scanner):
    def __init__(self, contract_address, *args, **kwargs):
        super().__init__(
            w3=config.POLYGON_URL, contract_address=contract_address, *args, **kwargs
        )
