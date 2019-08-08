#!/usr/bin/env python3

"""
main.py

Main script of Casket for parse argument and start the program.
"""

__authors__ = "Jasoc"
__version__ = "0.1-beta1"
__license__ = "GPL-3.0"


import os
import argparse

from logzero import logger

from Casket import Casket


def main():
    """ Main function Casket. """

    logger.info("Starting Casket")

    parser = argparse.ArgumentParser(description='Casket ' + __version__)

    # Casket [-c] [--commandline]
    parser.add_argument('-c', '--commandline', help='start Casket in CLI mode', action="store_true")

    # Casket [-v] [--version]
    parser.add_argument('-v', '--version', help='display version', action="store_true")

    args = parser.parse_args()

    if not os.path.isdir(Casket.HOME_PATH):     # Checking if this is first start of Casket
        Casket.firstSetup()                     # if true show up first setup window.

    # Check arguments for properly start Casket
    # or show some info

    if args.commandline:
        Casket.startCli()

    elif args.version:
        print('Casket ' + __version__)

    else:
        logger.info("Starting Casket GUI mode")
        Casket.startGui()     # If no argument is passed, start Casket in default GUI mode.


if __name__ == '__main__':
    main()
