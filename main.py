#!/usr/bin/env python3
import sys

import yaml

from src.classes.input_helper import InputHelper
from src.classes.jellyfin import Jellyfin
from src.classes.parseargs import ParseArgs


def update_config(config_file: str, config: dict) -> bool:
    try:
        with open(config_file, 'w') as file:
            yaml.safe_dump(config, file)
        return True
    except BaseException:
        return False


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
            exit(0)
        exit(1)

    elif action == 'cleanup':
        credentials_file = myparser.credentials
        jellyfin = Jellyfin(credentials_file)

        if jellyfin.userid is None:
            print('You need to configure a User ID!')
            result = jellyfin.users()
            if not result:
                exit(1)

            users = []
            for item in jellyfin.user_list:
                username = item['Name']
                userid = item['Id']
                user = (username, userid)
                users.append(user)
            ih = InputHelper()
            userid = ih.choose_user(users)
            if not userid:
                print('Unable to choose a User ID!')
                exit(1)

            print('Updating User ID...')
            jellyfin.config['jellyfin']['userid'] = userid
            jellyfin.userid = userid
            result = update_config(jellyfin.credentials_file, jellyfin.config)
            if not result:
                print('Unable to update config with User ID!')
                exit(1)

        if jellyfin.viewids is None:
            print('You need to configure at least 1 Library!')
            result = jellyfin.views()
            if not result:
                exit(1)

            views = []
            for item in jellyfin.view_list['Items']:
                viewname = item['Name']
                viewid = item['Id']
                view = (viewname, viewid)
                views.append(view)
            ih = InputHelper()
            viewids = ih.choose_view(views)
            if len(viewids) == 0:
                print('Unable to choose a Library!')
                exit(1)

            print('Updating Library IDs...')
            jellyfin.config['jellyfin']['viewids'] = viewids
            jellyfin.viewids = viewids
            result = update_config(jellyfin.credentials_file, jellyfin.config)
            if not result:
                print('Unable to update config with Library IDs!')
                exit(1)

        result = jellyfin.items()
        if not result:
            print('Failed getting a list of Items!')
            exit(1)

        result = jellyfin.remove()
        if not result:
            print('Failed to remove items!')
            exit(1)


if __name__ == '__main__':
    main()
