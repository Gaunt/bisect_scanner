from abc import ABC, abstractmethod
import bisect


class BaseScanner(ABC):
    def __init__(self, precission=3, interpolation_step=0, scan_step=1):
        self.interpolation_step = interpolation_step
        self.scan_step = scan_step
        self.precission = precission

    @abstractmethod
    def block_balance(self, block: int):
        pass

    @abstractmethod
    def last_block(self):
        pass

    def _balance_history(
        self,
        start_block,
        end_block,
    ):
        diff = end_block - start_block
        mid = start_block + diff // 2
        start_balance = self.block_balance(start_block)
        end_balance = self.block_balance(end_block)
        if abs(start_balance - end_balance) > self.interpolation_step:
            if diff > self.scan_step:
                yield from self._balance_history(start_block, mid)
                yield from self._balance_history(mid, end_block)
            elif self.interpolation_step:
                yield start_block, start_balance
                yield end_block, end_balance
            else:
                yield end_block, end_balance
        elif self.interpolation_step and start_balance != end_balance:
            yield mid, round((end_balance + start_balance) / 2, self.precission)

    def balance_history(
        self,
        start_block=0,
        end_block=None,
    ):
        if not end_block:
            end_block = self.last_block()
        yield start_block, self.block_balance(start_block)
        yield from self._balance_history(start_block, end_block)


class FakeChainScanner(BaseScanner):
    def __init__(self, BLOCK_BALANCES, *args, **kwargs):
        self.BLOCK_BALANCES = BLOCK_BALANCES
        self.BLOCKS, self.BALANCES = zip(*BLOCK_BALANCES)
        super().__init__(*args, **kwargs)

    def block_balance(self, block: int):
        if block <= 0:
            return 0
        i = bisect.bisect_left(self.BLOCKS, block) - 1
        return round(self.BLOCK_BALANCES[i][1], self.precission)

    def last_block(self):
        return self.BLOCKS[-1]
