#!/usr/bin/env python3
import logging
import logging.config
import os
import socket
import sys
from datetime import datetime

import yaml

from src.classes.file_checker import FileChecker
from src.classes.input_helper import InputHelper
from src.classes.jellyfin import Jellyfin
from src.classes.parseargs import ParseArgs
from src.constants import constants


def get_hostname() -> str:
    return socket.gethostname()


def get_pid() -> int:
    return os.getpid()


def update_config(config_file: str, config: dict) -> bool:
    try:
        with open(config_file, 'w') as file:
            yaml.safe_dump(config, file)
        return True
    except BaseException:
        return False


def main():
    base_path = os.path.realpath(os.path.dirname(__file__))
    logger_conf = f'{base_path}/src/configs/logging.conf'
    fc = FileChecker(logger_conf)
    logging.config.fileConfig(fc.file)
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.event_date = datetime.now().strftime(
            constants.EVENT_DATE_FORMAT)
        record.hostname = get_hostname()
        record.program = constants.ARGPARSE_PROGRAM_NAME
        record.pid = get_pid()
        return record

    logging.setLogRecordFactory(record_factory)
    logger = logging.getLogger('jellyfinCleanup')

    logger.info('Starting script...')

    args = sys.argv
    myparser = ParseArgs(args)
    action = myparser.action

    if action == 'test':
        logger.info('Running in test mode...')
        credentials_file = myparser.credentials
        jellyfin = Jellyfin(credentials_file)
        result = jellyfin.test()
        if result:
            print('Your credentials work!')
            logger.info('Your credentials work!')
            exit(0)
        exit(1)

    elif action == 'cleanup':
        logger.info('Running in cleanup mode...')
        credentials_file = myparser.credentials
        jellyfin = Jellyfin(credentials_file)

        if jellyfin.userid is None:
            print('You need to configure a User ID!')
            logger.info('ERROR: You need to configure a User ID!')
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
            logger.info('ERROR: You need to configure at least 1 Library!')
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
            logger.info('ERROR: Unable to get a list of Items!')
            exit(1)

        result = jellyfin.remove()
        if not result:
            print('Failed to remove items!')
            logger.info('ERROR: Unable to remove items!')
            exit(1)

    logger.info('Script finished successfully!')


if __name__ == '__main__':
    main()
