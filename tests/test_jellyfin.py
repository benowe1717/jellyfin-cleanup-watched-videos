#!/usr/bin/env python3
import os
from re import template

import pytest

from src.classes.jellyfin import Jellyfin
from src.constants import constants


class TestJellyfin:
    def setUp(self):
        self.credentials_file = 'tests/data/credentials.yaml'
        self.jf = Jellyfin(self.credentials_file)

    def tearDown(self):
        del self.jf
        del self.credentials_file

    def test_missing_credentials_file(self):
        file = '/some/fake/file'
        with pytest.raises(ValueError):
            Jellyfin(file)

    def test_invalid_credentials_file_not_a_file(self):
        file = '~/Documents/'
        with pytest.raises(ValueError):
            Jellyfin(file)

    def test_invalid_credentials_file_not_readable(self, monkeypatch):
        def mock_return(path, mode):
            return False
        monkeypatch.setattr(os, 'access', mock_return)
        file = 'tests/data/credentials.yaml'
        with pytest.raises(ValueError):
            Jellyfin(file)

    def test_invalid_credentials_file_not_yaml(self):
        file = 'tests/data/not_yaml.yaml'
        with pytest.raises(ValueError):
            Jellyfin(file)

    def test_invalid_credentials_file_invalid_file(self):
        file = 'tests/data/invalid_credentials.yaml'
        with pytest.raises(ValueError):
            Jellyfin(file)

    def test_invalid_credentials_file_missing_key(self):
        file = 'tests/data/missing_credentials.yaml'
        with pytest.raises(ValueError):
            Jellyfin(file)

    def test_invalid_credentials_file_additional_data(self):
        file = 'tests/data/additional_credentials.yaml'
        with pytest.raises(ValueError):
            Jellyfin(file)

    def test_credentials_file(self):
        self.setUp()
        assert self.jf.credentials_file == os.path.realpath(
            self.credentials_file)
        assert self.jf.host == 'subdomain.domain.tld'
        assert self.jf.apikey == '0f219ab50824a2c5de8360c2473eafe4'
        self.tearDown()

    def test_headers(self):
        self.setUp()
        assert len(self.jf.headers) == 3
        assert 'Accept' in self.jf.headers.keys()
        assert 'Host' in self.jf.headers.keys()
        assert 'X-Emby-Token' in self.jf.headers.keys()
        assert self.jf.headers['Accept'] == 'application/json'
        assert self.jf.headers['Host'] == 'subdomain.domain.tld'
        assert self.jf.headers['X-Emby-Token'] == '0f219ab50824a2c5de8360c2473eafe4'
        self.tearDown()

    def test_test_failed_unauthenticated(self, requests_mock):
        self.setUp()
        endpoint = '/System/Info'
        url = constants.JELLYFIN_API_SCHEME + self.jf.host + endpoint
        status_code = 401
        requests_mock.register_uri(
            'GET', url, text='', status_code=status_code)
        result = self.jf.test()
        assert result is False
        self.tearDown()

    def test_test_failed_forbidden(self, requests_mock):
        self.setUp()
        endpoint = '/System/Info'
        url = constants.JELLYFIN_API_SCHEME + self.jf.host + endpoint
        status_code = 403
        with open('tests/data/403_response.json', 'r') as file:
            data = file.read()
        requests_mock.register_uri(
            'GET', url, text=data, status_code=status_code)
        result = self.jf.test()
        assert result is False
        self.tearDown()

    def test_test(self, requests_mock):
        self.setUp()
        endpoint = '/System/Info'
        url = constants.JELLYFIN_API_SCHEME + self.jf.host + endpoint
        status_code = 200
        with open('tests/data/info_response.json', 'r') as file:
            data = file.read()
        requests_mock.register_uri(
            'GET', url, text=data, status_code=status_code)
        result = self.jf.test()
        assert result is True
        self.tearDown()

    def test_users_failed_unauthenticated(self, requests_mock):
        self.setUp()
        endpoint = '/Users'
        url = constants.JELLYFIN_API_SCHEME + self.jf.host + endpoint
        status_code = 401
        requests_mock.register_uri(
            'GET', url, text='', status_code=status_code)
        result = self.jf.users()
        assert result is False
        self.tearDown()

    def test_users_failed_forbidden(self, requests_mock):
        self.setUp()
        endpoint = '/Users'
        url = constants.JELLYFIN_API_SCHEME + self.jf.host + endpoint
        status_code = 403
        requests_mock.register_uri(
            'GET', url, text='', status_code=status_code)
        result = self.jf.users()
        assert result is False
        self.tearDown()

    def test_users(self, requests_mock):
        self.setUp()
        endpoint = '/Users'
        url = constants.JELLYFIN_API_SCHEME + self.jf.host + endpoint
        status_code = 200
        with open('tests/data/users_response.json', 'r') as file:
            data = file.read()
        requests_mock.register_uri(
            'GET', url, text=data, status_code=status_code)
        result = self.jf.users()
        assert result is True
        assert len(self.jf.user_list) == 1
        assert 'Name' in self.jf.user_list[0].keys()
        assert 'Id' in self.jf.user_list[0].keys()
        assert self.jf.user_list[0]['Name'] == 'string'
        assert self.jf.user_list[0]['Id'] == '38a5a5bb-dc30-49a2-b175-1de0d1488c43'
        self.tearDown()

    def test_views_failed_unauthenticated(self, requests_mock):
        self.setUp()
        endpoint = f'/Users/{self.jf.userid}/Views'
        url = constants.JELLYFIN_API_SCHEME + self.jf.host + endpoint
        status_code = 401
        requests_mock.register_uri(
            'GET', url, text='', status_code=status_code)
        result = self.jf.views()
        assert result is False
        self.tearDown()

    def test_views_failed_bad_request(self, requests_mock):
        self.setUp()
        endpoint = f'/Users/{self.jf.userid}/Views'
        url = constants.JELLYFIN_API_SCHEME + self.jf.host + endpoint
        status_code = 400
        data = 'Error processing request.'
        requests_mock.register_uri(
            'GET', url, text=data, status_code=status_code)
        result = self.jf.views()
        assert result is False
        self.tearDown()

    def test_views(self, requests_mock):
        self.setUp()
        endpoint = f'/Users/{self.jf.userid}/Views'
        url = constants.JELLYFIN_API_SCHEME + self.jf.host + endpoint
        status_code = 200
        with open('tests/data/views_response.json', 'r') as file:
            data = file.read()
        requests_mock.register_uri(
            'GET', url, text=data, status_code=status_code)
        result = self.jf.views()
        assert result is True
        views = self.jf.view_list['Items']
        assert len(views) == 1
        self.tearDown()
