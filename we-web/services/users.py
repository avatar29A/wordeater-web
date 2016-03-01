# coding=utf-8
__author__ = 'Warlock'

from services.base import BaseService
from logger import logger


class UserService(BaseService):

    def list(self):
        """
        Returns all users from database
        :return: list of User
        """

        return list(self.connection.User.find())

    def count(self):
        """
        Returns count users in collection
        :return: count users in collection
        """

        return self.connection.User.find().count()

    def create(self, login,
               native=u'ru',
               foreign=u'en',
               first_name=u'anonymous',
               last_name=u'anonymous',
               sex=u'male'):
        """
        Create a new user
        :param login:
        :param native: Native user language
        :param foreign: Foreign language for user
        :param sex: sex
        :return: user entity
        """

        user = self.get(login)

        if user is not None:
            return user

        user = self.connection.User()
        user.login = login
        user.name.last_name = first_name
        user.name.first_name = last_name

        user.sex = sex
        user.native_lng = native
        user.foreign_lng = foreign

        try:
            user.validate()
            user.save()

            return user
        except Exception as ex:
            logger.error(ex.message)

            return None

    def prepare(self, user):
        """
        Init default state for Demo
        :param user: current user
        :return:
        """

    def clear(self):
        """
        Remove all records from User collection
        :return: Count remove records
        """

        count = self.connection.User.find().drop()

        try:
            self.connection.User.remove()
        except Exception as ex:
            logger.error(ex.message)

            return 0

        return count

    def exists(self, login):
        """
        Check user exits in database
        :param login: user login
        :return: true or false
        """
        return self.connection.User.find_one({'login': login}) is not None

    def get(self, login):
        """
        Return user from User collection
        :param login: user's login
        :return: User entity
        """

        return self.connection.User.find_one({'login': login})

