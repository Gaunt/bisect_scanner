import configparser
from json import load
from pathlib import Path
from types import SimpleNamespace
import os

from _pytest import config


CONFIG_PATH = Path(os.path.expanduser("~")) / ".config/bisect_scanner.ini"
CONFIG_SECTION = 'node_urls'


def get_conf_val(conf, name):
    try:
        section = conf['node_urls']
    except:
        section = {}
    return section.get(name) or os.environ.get('BISECTSCANNER_' + name)


class Config:
    def __init__(self, config_path=CONFIG_PATH):
        self.config = load_config(config_path)
        self.W3_URL = get_conf_val(self.config, 'W3_URL')
        self.POLYGON_URL = get_conf_val(self.config, 'POLYGON_URL')
        self.ETHEREUM_URL = get_conf_val(self.config, 'ETHEREUM_URL')


def load_config(config_path=CONFIG_PATH):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


config = None
def configure():
    global config
    config = Config(config_path=CONFIG_PATH)
