#!/usr/bin/env python3
import os

import pytest

from src.classes.file_checker import FileChecker


class TestFileChecker:
    def setUp(self):
        self.file = 'tests/data/credentials.yaml'
        self.fc = FileChecker(self.file)

    def tearDown(self):
        del self.fc
        del self.file

    def test_file_on_startup_missing_file_failed(self):
        file = '/some/fake/file'
        with pytest.raises(ValueError):
            fc = FileChecker(file)
            print(fc.file)
            assert fc.file == ''

    def test_file_on_startup_relative_path_with_period(self):
        path = '/home/benjamin/Documents/github/jellyfin-cleanup-watched-videos/tests/data'
        file = './tests/data/credentials.yaml'
        fc = FileChecker(file)
        assert fc.file == f'{path}/credentials.yaml'

    def test_file_on_startup_relative_path_no_period(self):
        path = '/home/benjamin/Documents/github/jellyfin-cleanup-watched-videos/tests/data'
        file = 'tests/data/credentials.yaml'
        fc = FileChecker(file)
        assert fc.file == f'{path}/credentials.yaml'

    def test_file_on_startup_user_path(self):
        path = '/home/benjamin/Documents/github/jellyfin-cleanup-watched-videos/tests/data'
        file = '~/Documents/github/jellyfin-cleanup-watched-videos/tests/data/credentials.yaml'
        fc = FileChecker(file)
        assert fc.file == f'{path}/credentials.yaml'

    def test_file_on_startup_absolute_path(self):
        path = '/home/benjamin/Documents/github/jellyfin-cleanup-watched-videos/tests/data'
        file = '/credentials.yaml'
        filepath = path + file
        fc = FileChecker(filepath)
        assert fc.file == filepath

    def test_is_file_not_a_file(self):
        file = '~/Documents/'
        fc = FileChecker(file)
        assert fc.is_file() is False

    def test_is_file(self):
        self.setUp()
        assert self.fc.is_file() is True
        self.tearDown()

    def test_is_readable_is_not_readable_permissions(self, monkeypatch):
        def mock_return(path, mode):
            return False
        monkeypatch.setattr(os, 'access', mock_return)

        self.setUp()
        fc = FileChecker(self.file)
        assert fc.is_readable() is False
        self.tearDown()

    def test_is_readable_is_not_readable_ownership(self, monkeypatch):
        def mock_return(path, mode):
            return False
        monkeypatch.setattr(os, 'access', mock_return)

        self.setUp()
        fc = FileChecker(self.file)
        assert fc.is_readable() is False
        self.tearDown()

    def test_is_readable(self):
        self.setUp()
        assert self.fc.is_readable() is True
        self.tearDown()

    def test_is_yaml_not_yaml(self):
        file = 'tests/data/not_yaml.yaml'
        fc = FileChecker(file)
        assert fc.is_yaml() is False

    def test_is_yaml(self):
        self.setUp()
        result = self.fc.is_yaml()
        assert result is True
        assert isinstance(self.fc.data, dict)
        assert 'credentials' in self.fc.data.keys()
        creds = self.fc.data['credentials']
        assert 'host' in creds.keys()
        assert 'apikey' in creds.keys()
        assert creds['host'] == 'subdomain.domain.tld'
        assert creds['apikey'] == '0f219ab50824a2c5de8360c2473eafe4'
        self.tearDown()
