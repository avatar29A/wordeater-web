# coding=utf-8
from services.base import BaseService
from logger import logger

__author__ = 'Warlock'


class UserService(BaseService):

    def single(self, login):
        """
        Return user from User collection
        :param login: user's login
        :return: User entity
        """

        return self.db.User.find_one({'login': login})

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
        :param first_name: -
        :param last_name: -
        :param sex: sex
        :return: user entity
        """

        user = self.single(login)

        if user is not None:
            return user

        user = self.db.User()

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
            logger.error(u"UserService.create", ex)
            return None

    def exists(self, login):
        """
        Check user exits in database
        :param login: user login
        :return: true or false
        """
        return self.db.User.find_one({'login': login}) is not None
