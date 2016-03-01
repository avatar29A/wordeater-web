# coding=utf-8
from model import *


@db.register
class User(BaseDocument):
    __collection__ = "users"

    structure = {
        'login': unicode,
        'name': {
            'first_name': unicode,
            'last_name': unicode
        },

        'sex': IS(*enums.SEX),
        'native_lng': IS(*enums.LANGUAGE),
        'foreign_lng': IS(*enums.LANGUAGE),
        'create_date': datetime.datetime
    }

    default_values = {
        'create_date': datetime.datetime.now()
    }

    indexes = [
        {
            'fields': ['login'],
            'unique': True
        }]

    @property
    def cards(self):
        return list(db.Card.find({"user.$id": self.id}))

    @staticmethod
    def single(login):
        """
        Return user from User collection
        :param login: user's login
        :return: User entity
        """

        return db.User.find_one({'login': login})

    @staticmethod
    def all():
        """
        Returns all users from database
        :return: list of User
        """

        return list(db.User.find())

    @staticmethod
    def count():
        """
        Returns count users in collection
        :return: count users in collection
        """

        return db.User.find().count()

    @staticmethod
    def create(login,
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

        user = User.single(login)

        if user is not None:
            return user

        user = db.User()

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
            logger.error("User.create", ex)
            return None

    @staticmethod
    def exists(login):
        """
        Check user exits in database
        :param login: user login
        :return: true or false
        """
        return db.User.find_one({'login': login}) is not None

