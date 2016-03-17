# coding=utf-8

__author__ = 'Glebov Boris'


class EmailAlreadyExists(Exception):
    pass


class LoginAlreadyExists(Exception):
    pass


class TranslateError(Exception):
    def __init__(self, response, *args, **kwargs):
        self.response = response

        Exception.__init__(*args, **kwargs)
