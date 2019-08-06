#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from casket import firstSetup, Account, CryptoUtils, startGui, CASKET
from casket.interface import IMain


VERSION = '0.1-beta1'


def PRINT_HELP():
    sys.stderr.write("""
Casket %s

Usage: casket [OPTION] [ACCOUNT]

OPTION include:

    -cli       -C    Start casket in CLI mode
    -help      -H    Show help
    -version   -V    Display version

ACCOUNT is the name of account you want to manage. \n
""" % (VERSION))


def main():

    if not os.path.isdir(CASKET.HOME_PATH):
        firstSetup()

    if len(sys.argv) == 1:
        startGui()

    elif '-cli' in sys.argv or '-C' in sys.argv:

        if len(sys.argv) == 4:
            pass

        else:
            raise Exception('Missing arguments.')

    elif '-help' in sys.argv or '-H' in sys.argv:

        PRINT_HELP()
    elif '-version' in sys.argv or '-V' in sys.argv:
        print('Casket ' + VERSION)

    else:
        print('Invalid arguments.')
        PRINT_HELP()


if __name__ == '__main__':
    main()
