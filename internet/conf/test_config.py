import os

from .config import load


def test_loading():
    cfg = load()

    assert cfg.database.host == '127.0.0.1'
    assert cfg.database.port == 3306
    assert cfg.database.database == 'radius'

def test_loading_with_env():
    os.environ['INTERNET_DATABASE__PORT'] = '3307'
    os.environ['INTERNET_DATABASE__HOST'] = 'localhost'

    cfg = load()

    assert cfg.database.host == 'localhost'
    assert cfg.database.port == 3307
    assert cfg.database.database == 'radius'
