#!/usr/bin/env python3
import sys

from src.classes.jellyfin import Jellyfin
from src.classes.parseargs import ParseArgs


def main():
    args = sys.argv
    myparser = ParseArgs(args)
    action = myparser.action

    if action == 'test':
        credentials_file = myparser.credentials
        jellyfin = Jellyfin(credentials_file)
        result = jellyfin.test()
        if result:
            print('Your credentials work!')


if __name__ == '__main__':
    main()
