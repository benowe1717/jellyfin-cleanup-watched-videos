#!/usr/bin/env python3
import sys

from src.classes.parseargs import ParseArgs


def main():
    args = sys.argv
    myparser = ParseArgs(args)


if __name__ == '__main__':
    main()
