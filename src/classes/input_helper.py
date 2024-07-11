#!/usr/bin/env python3

class InputHelper():
    def __init__(self) -> None:
        pass

    def _get_usernames(self, data: list) -> list:
        usernames = []
        for item in data:
            username = item[0]
            usernames.append(username)
        usernames.sort()
        return usernames

    def _validate_choice(self, choices: list, choice: int) -> bool:
        total = len(choices)
        if choice >= 0 and choice <= (total - 1):
            return True
        return False

    def _print_list(self, data: list) -> None:
        i = 0
        total = len(data)
        while i < total:
            print(f'[{i}] {data[i]}')
            i += 1

    def _get_userid_from_username(self, users: list, username: str) -> str:
        for user in users:
            if user[0] == username:
                return user[1]
        return ''

    def choose_user(self, data: list) -> str:
        while True:
            usernames = self._get_usernames(data)
            self._print_list(usernames)
            choice = input(
                'Enter the number of the User you want to use: ').strip()

            try:
                choice = int(choice)
                result = self._validate_choice(usernames, choice)
                if not result:
                    print('That is not a valid choice!')
                    continue

                username = usernames[choice]
                userid = self._get_userid_from_username(data, username)
                return userid
            except BaseException:
                print('That is not a valid number!')
                continue
