# coding=utf-8

from services.base import BaseService
from services.service_locator import ServiceLocator
from utils.session_manager import UserSession
from flask import session

__author__ = 'Warlock'


class SessionService(BaseService):
    #
    # Public methods

    def create(self, user, token):
        """
        Create DTO for Session storage and adds it to Session.
        :param user: User entity from DB
        :return: UserSession
        """

        session['user'] = {
            'id': str(user.id),
            'login': user.login,
            'token': token
        }

        return UserSession.create(session['user'])

    def get(self):
        """
        Returns UserSession instance
        :return:
        """

        if 'user' not in session:
            return None

        return UserSession(UserSession.get_current_user())

    def get_user(self):
        """
        Return user entity from DB by user' id from Session
        :return: User entity
        """

        user_session = self.get()
        if not user_session:
            return None

        us = ServiceLocator.resolve(ServiceLocator.USERS)
        return us.single(user_session.login)
