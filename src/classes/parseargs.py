#!/usr/bin/env python3
import argparse

from src.classes.file_checker import FileChecker
from src.constants import constants


class ParseArgs():
    NAME = constants.ARGPARSE_PROGRAM_NAME
    DESC = constants.ARGPARSE_PROGRAM_DESCRIPTION
    VERSION = constants.ARGPARSE_VERSION
    AUTHOR = constants.ARGPARSE_AUTHOR
    REPO = constants.ARGPARSE_REPO

    def __init__(self, args) -> None:
        self.errors = []
        self.action = ''
        self.credentials = ''
        self.args = args
        self.parser = argparse.ArgumentParser(
            prog=self.NAME, description=self.DESC)

        self.parser.add_argument(
            '-v',
            '--version',
            action='store_true',
            required=False,
            help='Show this program\'s current version')

        self.parser.add_argument(
            '-e',
            '--credentials',
            nargs=1,
            help='The file containing your API credentials'
        )

        self.parser.add_argument(
            '-t',
            '--test',
            action='store_true',
            required=False,
            help='Test the provided credentials against the Jellyfin API'
        )

        self.parser.add_argument(
            '-c',
            '--cleanup',
            action='store_true',
            required=False,
            help='Cleanup watched videos'
        )

        self.parse_args = self.parser.parse_args()

        if len(self.args) == 1:
            self.parser.print_help()
            self.parser.exit()

        if self.parse_args.version:
            self._print_version()
            self.parser.exit()

        if self.parse_args.test:
            self.action = 'test'
            if self.parse_args.credentials is None:
                self.parser.error('--test requires --credentials')

            result = self._is_valid_credentials_path(
                self.parse_args.credentials[0])
            if not result:
                self.parser.error('Invalid credentials file')

        if self.parse_args.cleanup:
            self.action = 'cleanup'
            if self.parse_args.credentials is None:
                self.parser.error('--test requires --credentials')

            result = self._is_valid_credentials_path(
                self.parse_args.credentials[0])
            if not result:
                self.parser.error('Invalid credentials file')

    def _print_version(self) -> None:
        print(f'{self.NAME} v{self.VERSION}')
        print(
            'This is free software:',
            'you are free to change and redistribute it.')
        print('There is NO WARARNTY, to the extent permitted by law.')
        print(f'Written by {self.AUTHOR}; see below for original code')
        print(f'<{self.REPO}')

    def _is_valid_credentials_path(self, path) -> bool:
        try:
            fc = FileChecker(path)
            if not fc.is_file():
                return False

            if not fc.is_readable():
                return False

            if not fc.is_yaml():
                return False

            self.credentials = fc.file
            return True
        except ValueError:
            return False
