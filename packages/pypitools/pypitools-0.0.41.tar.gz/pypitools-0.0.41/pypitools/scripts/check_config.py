"""
This script checks your config file
"""

import click

from pypitools import common


@click.command()
def main():
    """
    This script checks your config file
    """
    common.setup_main()
    common.ConfigData()


if __name__ == '__main__':
    main()
