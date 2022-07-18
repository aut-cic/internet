'''
runs internet server
'''

from rich import pretty
from rich.console import Console

import internet.conf

if __name__ == '__main__':
    console = Console()
    pretty.install()

    cfg = internet.conf.load()
    pretty.pprint(cfg)
