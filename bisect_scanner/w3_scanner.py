import time
import json
import os
from pathlib import Path
from functools import lru_cache
from typing import Union
import web3
from dotenv import load_dotenv
from bisect_scanner.base_scanner import BaseScanner, FakeChainScanner
import requests


user_config = Path(os.path.expanduser("~")) / ".config/bisect_scanner_rc"


if user_config.exists():
    load_dotenv(user_config)


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


@lru_cache(1000)
def get_abi(contract_address):
    url = (
        f"https://api.etherscan.io/api"
        "?module=contract&action=getabi&address={contract_address}"
    )
    res = requests.get(url)
    return res.json()["result"]


def get_contract_balance(w3, contract_address, account, block):
    contract_address = web3.Web3.toChecksumAddress(contract_address)
    # abi = get_abi(contract_address)
    contract = w3.eth.contract(address=contract_address, abi=ABI)
    return contract.functions.balanceOf(account).call(block_identifier=block)


def get_contract_decimals(w3, contract_address):
    contract_address = web3.Web3.toChecksumAddress(contract_address)
    contract = w3.eth.contract(address=contract_address, abi=ABI)
    return contract.functions.decimals().call()


class W3Scanner(BaseScanner):
    def __init__(
        self,
        account=None,
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
        self.account = account
        if contract_address:
            self.decimals = get_contract_decimals(self.web3, contract_address)
        else:
            self.decimals = DECIMALS
        super().__init__(*args, **kwargs)

    @lru_cache(CACHE_SIZE)
    def block_balance(self, block):
        time.sleep(DELAY)
        if self.contract_address:
            balance = self.token_balance(
                self.account, block, self.contract_address
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


class EtherScanner(W3Scanner):
    def __init__(self, *args, **kwargs):
        ETHEREUM_URL = os.getenv("ETHEREUM_URL", "")
        super().__init__(w3=ETHEREUM_URL, *args, **kwargs)


class PolygonScanner(W3Scanner):
    def __init__(self, *args, **kwargs):
        POLYGON_URL = os.getenv("POLYGON_URL", "")
        super().__init__(w3=POLYGON_URL, *args, **kwargs)


class EthereumERC20Scanner(W3Scanner):
    def __init__(self, contract_address, *args, **kwargs):
        ETHEREUM_URL = os.getenv("ETHEREUM_URL", "")
        super().__init__(
            w3=ETHEREUM_URL, contract_address=contract_address, *args, **kwargs
        )


class PolygonERC20Scanner(W3Scanner):
    def __init__(self, contract_address, *args, **kwargs):
        POLYGON_URL = os.getenv("POLYGON_URL", "")
        super().__init__(
            w3=POLYGON_URL, contract_address=contract_address, *args, **kwargs
        )
