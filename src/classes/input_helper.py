#!/usr/bin/env python3

class InputHelper():
    def __init__(self) -> None:
        pass

    def _go_again(self, msg: str) -> bool:
        again = input(f'{msg} [Yes/no]: ')
        again = again.lower().strip()
        if again == 'no' or again == 'n':
            return False
        elif again != 'yes' and again != 'y':
            print('That was not a valid response! ' + 'Stopping anyways...')
            return False
        else:
            return True

    def _get_usernames(self, data: list) -> list:
        usernames = []
        for item in data:
            username = item[0]
            usernames.append(username)
        usernames.sort()
        return usernames

    def _get_viewnames(self, data: list) -> list:
        viewnames = []
        for item in data:
            viewname = item[0]
            viewnames.append(viewname)
        viewnames.sort()
        return viewnames

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

    def _get_viewid_from_viewname(self, views: list, viewname: str) -> str:
        for view in views:
            if view[0] == viewname:
                return view[1]
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

    def choose_view(self, data: list) -> list:
        viewids = []
        more = True
        msg = 'Do you want to add another Library?'
        while more:
            viewnames = self._get_viewnames(data)
            self._print_list(viewnames)
            choice = input(
                'Enter the number of the Library you want to use: '
            ).strip()

            try:
                choice = int(choice)
                result = self._validate_choice(viewnames, choice)
                if not result:
                    print('That is not a valid choice!')
                    continue

                viewname = viewnames[choice]
                viewid = self._get_viewid_from_viewname(data, viewname)
                if not viewid:
                    print('That is not a valid Library!')
                    continue

                viewids.append(viewid)
            except BaseException:
                print('That is not a valid number!')
                continue

            if not self._go_again(msg):
                more = False
        return viewids
