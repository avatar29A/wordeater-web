# coding=utf-8
import config

from services.base import BaseService
from logger import logger
from itsdangerous import TimedJSONWebSignatureSerializer as TokenSerializer, BadSignature, SignatureExpired

__author__ = 'Warlock'


class UserService(BaseService):

    #
    # Public interfaces

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

        assert login, u'Login is required parameter'

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

    def single(self, login):
        """
        Return user from User collection
        :param login: user's login
        :return: User entity
        """

        assert login, u'Login is required parameter'

        return self.db.User.find_one({'login': login})

    def exists(self, login):
        """
        Check user exits in database
        :param login: user login
        :return: true or false
        """
        return self.single(login) is not None

    def sign_in(self, login):
        """
        Authorization in system.

        Firs stage: Required only user login. If user is doesn't exist, he will be created.
        :return:
        """
        assert login

        return self.create(login)

    def make_auth_token(self, user):
        """
        Generate new security user token for user
        :param user: User
        :return: Token
        """

        s = TokenSerializer(config.SECRET_KEY, expires_in=config.SESSION_EXPIRES)

        return s.dumps({u'login': user[u'login']})

    def verify_auth_token(self, token):
        """
        Token verification. Check token by expires and valid.
        :param token: token
        :return: user's login
        """

        s = TokenSerializer(config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        return data[u'login']
