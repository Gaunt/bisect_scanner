import eth_tester.backends.mock.main as mock_backend
import eth_tester.backends.mock.factory as factory

DEFAULT_ALLOC = 0

ACCOUNT_DEFAULTS = {
        'balance': DEFAULT_ALLOC * mock_backend.denoms.ether,
        'code': b'',
        'nonce': 0,
        'storage': {},
    }


POLYGON_GENESIS = factory.make_genesis_block()


def update_defaults(**kwargs):
    ACCOUNT_DEFAULTS.update(**kwargs)


def account_defaults():
    return ACCOUNT_DEFAULTS
