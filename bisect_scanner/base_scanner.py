from os import access
from typing import List, Tuple, Union
from abc import ABC, abstractmethod
from more_itertools import windowed
from bisect_scanner import util
import bisect


DEFAULT_SITUATION_SCAN_STEPS = 30


def validate_address(address):
    if util.check_addr(address):
        raise ValueError(f'Address {address} seems to be invalid')


class BaseScanner(ABC):
    def __init__(
        self, precission=3, interpolation_step=0, scan_step=1
    ):
        self.interpolation_step = interpolation_step
        self.scan_step = scan_step
        self.precission = precission

    @abstractmethod
    def block_balance(self, account, block: int) -> float:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def last_block(self) -> int:
        raise NotImplementedError  # pragma: no cover

    def _balance_history(
        self,
        account,
        start_block,
        end_block,
    ):
        diff = end_block - start_block
        mid = start_block + diff // 2
        start_balance = self.block_balance(account, start_block)
        end_balance = self.block_balance(account, end_block)
        if start_balance is None and end_balance is None:
            return
        if (start_balance is None) or (
            abs(start_balance - end_balance) > self.interpolation_step
        ):
            if diff > self.scan_step:
                yield from self._balance_history(account, start_block, mid)
                yield from self._balance_history(account, mid, end_block)
            elif self.interpolation_step:
                yield start_block, start_balance
                yield end_block, end_balance
            else:
                yield end_block, end_balance
        elif self.interpolation_step and start_balance != end_balance:
            yield mid, round((end_balance + start_balance) / 2, self.precission)

    def balance_history(
        self,
        account: str,
        start_block=0,
        end_block=None,
        situation_scan_steps=0,
    ):
        if not end_block:
            end_block = self.last_block()
        start_balance = self.block_balance(account, start_block)
        end_balance = self.block_balance(account, end_block)
        if start_balance is not None:
            yield start_block, start_balance
        if end_balance == start_balance:
            situation_scan_steps = DEFAULT_SITUATION_SCAN_STEPS
        if situation_scan_steps:
            situation = self.situation_scan(
                account=account,
                start_block=start_block,
                end_block=end_block,
                steps=situation_scan_steps,
            )
            for (block1, balance1), (block2, balance2) in windowed(
                situation, 2
            ):
                yield from self._balance_history(account, block1, block2)
        else:
            yield from self._balance_history(account, start_block, end_block)

    def situation_scan(
            self, account, start_block=0, end_block=None, steps=100
    ):
        return util.uniq(
            self._situation_scan(
                start_block=start_block,
                end_block=end_block,
                account=account,
                steps=steps,
            )
        )

    def _situation_scan(
            self, account, start_block=0, end_block=None, steps=100
    ):
        if not end_block:
            end_block = self.last_block()
        scan_blocks = util.scan_steps(
            start_block=start_block, end_block=end_block, steps=steps
        )

        def block_balance(block):
            return self.block_balance(account, block)
        
        block_balances = zip(scan_blocks, map(block_balance, scan_blocks))
        for (prev_block, prev_balance), (block, balance) in windowed(
            block_balances, 2
        ):
            if prev_balance != balance:
                yield prev_block, prev_balance
                yield block, balance


class FakeChainScanner(BaseScanner):
    def __init__(
        self,
        block_balances: Union[None, List[Tuple[int, float]]] = None,
        *args,
        **kwargs,
    ):
        if block_balances:
            self.BLOCK_BALANCES = block_balances
        else:
            from bisect_scanner import example_data

            self.BLOCK_BALANCES = example_data.BLOCK_BALANCES
        self.BLOCKS, self.BALANCES = zip(*self.BLOCK_BALANCES)
        super().__init__(*args, **kwargs)

    def block_balance(self, account, block: int) -> float:
        validate_address(account)
        if block <= 0:
            return 0
        i = bisect.bisect_left(self.BLOCKS, block) - 1
        return round(self.BLOCK_BALANCES[i][1], self.precission)

    def last_block(self):
        return self.BLOCKS[-1]


class SlowedDownScanner(FakeChainScanner):
    def __init__(
        self,
        block_balances: Union[None, List[Tuple[int, float]]] = None,
        delay=0,
        *args,
        **kwargs,
    ):
        self.delay = delay
        super().__init__(block_balances, *args, **kwargs)

    def balance_history(
        self,
        account,
        start_block=0,
        end_block=None,
        situation_scan_steps=0,
    ):
        yield from util.slowed_down(
            super().balance_history(
                account=account,
                start_block=start_block,
                end_block=end_block,
                situation_scan_steps=situation_scan_steps,
            ),
            self.delay,
        )
