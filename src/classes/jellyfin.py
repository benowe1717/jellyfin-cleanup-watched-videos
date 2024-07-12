#!/usr/bin/env python3
import requests

from src.classes.file_checker import FileChecker
from src.constants import constants


class Jellyfin:
    SCHEME = constants.JELLYFIN_API_SCHEME

    def __init__(self, credentials_file: str) -> None:
        self.headers = {
            'Accept': 'application/json'
        }
        self.credentials_file = credentials_file
        self.user_list = []
        self.view_list = {}
        self.item_list = []

    @property
    def credentials_file(self) -> str:
        return self._credentials_file

    @credentials_file.setter
    def credentials_file(self, filepath: str) -> None:
        self._credentials_file = ''
        fc = FileChecker(filepath)
        if not fc.is_file():
            raise ValueError('Not a file')

        if not fc.is_readable():
            raise ValueError('Not readable')

        result = fc.is_yaml()
        if not result:
            raise ValueError('Not YAML')

        try:
            self.config = fc.data

            credentials = self.config['credentials']
            self._credentials_file = fc.file
            self.host = credentials['host']
            self.apikey = credentials['apikey']

            self.headers['Host'] = self.host
            self.headers['X-Emby-Token'] = self.apikey

            config = self.config['jellyfin']
            self.userid = config['userid']
            self.viewids = config['viewids']
            self.exclusions = config['exclusions']
        except KeyError:
            raise ValueError('Invalid credentials file')

    def _is_excluded(self, name: str) -> bool:
        if not self.exclusions:
            return False

        if len(self.exclusions) == 0:
            return False

        for item in self.exclusions:
            if item.lower() in name.lower():
                return True
        return False

    def test(self) -> bool:
        endpoint = '/System/Info'
        url = self.SCHEME + self.host + endpoint
        r = requests.get(url=url, headers=self.headers)
        if r.status_code == 401:
            print('401 Unauthorized')
            return False
        if r.status_code != 200:
            data = r.json()
            data['status_code'] = r.status_code
            print(', '.join('{}: {}'.format(key, value)
                  for key, value in data.items()))
            return False
        return True

    def users(self) -> bool:
        endpoint = '/Users'
        url = self.SCHEME + self.host + endpoint
        r = requests.get(url=url, headers=self.headers)
        if r.status_code != 200:
            print(r.status_code, r.text)
            return False
        self.user_list = r.json()
        return True

    def views(self) -> bool:
        endpoint = f'/Users/{self.userid}/Views'
        url = self.SCHEME + self.host + endpoint
        r = requests.get(url=url, headers=self.headers)
        if r.status_code == 401 or r.status_code == 400:
            print(r.status_code, r.text)
            return False
        if r.status_code != 200:
            data = r.json()
            data['status_code'] = r.status_code
            print(', '.join('{}: {}'.format(key, value)
                  for key, value in data.items()))
            return False
        self.view_list = r.json()
        return True

    def items(self) -> bool:
        errors = 0
        for viewid in self.viewids:
            endpoint = f'/Users/{self.userid}/Items'
            params = f'?Recursive=True&isPlayed=True&ParentId={viewid}'
            url = self.SCHEME + self.host + endpoint + params
            r = requests.get(url=url, headers=self.headers)
            if r.status_code == 401:
                print('401 Unauthorized')
                errors += 1
                continue

            if r.status_code != 200:
                data = r.json()
                data['status_code'] = r.status_code
                print(', '.join('{}: {}'.format(key, value)
                      for key, value in data.items()))
                errors += 1
                continue

            data = r.json()
            if data['TotalRecordCount'] == 0:
                continue

            for item in data['Items']:
                video_name = item['Name']
                video_id = item['Id']
                if not self._is_excluded(video_name):
                    video = (video_name, video_id)
                    self.item_list.append(video)

        if errors > 0:
            return False
        return True
