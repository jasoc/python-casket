#!/usr/bin/env python3
""" __main__.py
    Main script of Casket for parse argument and start the program.
"""
__authors__ = "Jasoc"
__version__ = "0.1b1"
__license__ = "GNU General Public License v3.0"

import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys
import argparse
import pickle
import casket

def main():
    """ Main function Casket. """
    casket.log("Starting casket.")
    parser = argparse.ArgumentParser(description='Casket ' + __version__)

    if not os.path.isdir(casket.home.HOME_PATH):           # Checking if this is first start of Casket
        casket.home.first_setup()                          # if true show up first setup window.

    parser.add_argument('-a', '--add-account', action="store_true", help='Add a new password to the database.')
    parser.add_argument('-l', '--accounts-list', action="store_true", help='Show all the saved accounts.')
    parser.add_argument('-r', '--remove-account', nargs='?', metavar="account", help='Remove the passed account from the database.')
    parser.add_argument('-g', '--get', nargs='?', metavar="account", help='Show account info from the database.')
    parser.add_argument('-c', '--configure', action="store_true", help='Set up your casket session.')
    args = parser.parse_args()

    if args.configure:
        if casket.home.first_start():
            while True:
                upswd = input('[**CASKET CONFIG**]: Insert your master password: ')
                ver_upswd = input('[**CASKET CONFIG**]: Confirm: ')
                if upswd == ver_upswd:
                    with open(casket.home.MASTER_HASH_PATH, 'wb') as filehandler:
                        pickle.dump(upswd, filehandler)
                    break
                else:
                    print('\n[**CASKET CONFIG**]: Two passwords doesen\'t match.\n')
                    continue
    elif args.add_account:
        pass
    elif args.accounts_list:
        pass
    elif args.remove_account:
        pass
    elif args.get:
        pass

if __name__ == '__main__':
    main()
