from json import load
from _pytest import config
import pytest
import os
from textwrap import dedent
from bisect_scanner.config import Config, load_config, configure
import bisect_scanner.config as config


@pytest.fixture
def valid_config_file(tmp_path):
    content = dedent("""
    [node_urls]
    W3_URL=wss://w3_url/ws
    POLYGON_URL=wss://polygon_url/ws
    ETHEREUM_URL=wss://ethereum_url/ws
    """)
    fn = tmp_path / 'valid.conf'
    with open(fn, 'w+') as f:
        f.write(content)
    return fn


@pytest.fixture
def invalid_config_file(tmp_path):
    content = dedent("""
    [urls]
    W3_URL=wss://w3_url/ws
    POLYGON_URL=wss://polygon_url/ws
    ETHEREUM_URL=wss://ethereum_url/ws
    """)
    fn = tmp_path / 'valid.conf'
    with open(fn, 'w+') as f:
        f.write(content)
    return fn


def test_load_config_valid(valid_config_file):
    config = load_config(valid_config_file)
    assert [*config['node_urls'].keys()] == ['w3_url', 'polygon_url', 'ethereum_url']
    assert config['node_urls']['W3_URL'] == "wss://w3_url/ws"
    assert config['node_urls']['POLYGON_URL'] == "wss://polygon_url/ws"
    assert config['node_urls']['ETHEREUM_URL'] == "wss://ethereum_url/ws"


def test_no_confg():
    config = Config()
    assert config.ETHEREUM_URL is None
    os.environ['BISECTSCANNER_ETHEREUM_URL'] = 'wss://url'
    config = Config()
    assert config.ETHEREUM_URL == 'wss://url'


def test_configure():
    os.environ['BISECTSCANNER_POLYGON_URL'] = 'wss://polygon_url'
    configure()
    assert config.config.POLYGON_URL == 'wss://polygon_url'
