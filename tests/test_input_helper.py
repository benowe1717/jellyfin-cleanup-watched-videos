#!/usr/bin/env python3
import pytest

from src.classes.input_helper import InputHelper


class TestInputHelper():
    def setUp(self):
        self.file = 'tests/data/credentials.yaml'
        self.ih = InputHelper()

    def tearDown(self):
        del self.ih
        del self.file

    def test_print_list(self, capsys):
        self.setUp()
        my_list = ['a ship', 'a cup', 'a jedi']
        output = '[0] a ship\n[1] a cup\n[2] a jedi\n'
        self.ih._print_list(my_list)
        captured = capsys.readouterr()
        assert captured.out == output
        self.tearDown()

    def test_validate_choice_failed(self):
        self.setUp()
        my_list = ['a ship', 'a cup', 'a jedi']
        choice = 5
        result = self.ih._validate_choice(my_list, choice)
        assert result is False
        self.tearDown()

    def test_validate_choice(self):
        self.setUp()
        my_list = ['a ship', 'a cup', 'a jedi']
        choice = 0
        result = self.ih._validate_choice(my_list, choice)
        assert result is True
        self.tearDown()
