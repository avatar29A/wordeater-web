# -*- coding: utf-8 -*-
from flask import session
__author__ = 'Glebov Boris'


class UserSession:
    def __init__(self, user):
        self.user = user

    @staticmethod
    def create():
        return UserSession(UserSession.get_current_user())

    def get(self):
        return self.user

    @property
    def id(self):
        return self.user['id']

    @property
    def login(self):
        return self.user['login']

    @property
    def email(self):
        return self.user['email']

    @property
    def remote_addr(self):
        return self.user['remote_addr']

    @staticmethod
    def get_current_user():
        """
        Extract session from current user
        """
        user = session.get('user')

        return user

    @staticmethod
    def check_user_auth():
        """
        Checks that user is authorized
        """
        user = session.get('user')

        if user is None or not user['is_auth']:
            return False

        return True
