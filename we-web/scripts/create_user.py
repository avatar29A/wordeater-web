# coding=utf-8
__author__ = 'Warlock'

from flask.ext.script import Command
from services.real.users import UserService


class CreateUser(Command):
    """
    Add new user with name Warlock
    """

    def run(self):
        print u"Run create user with name 'warlock'"

        us = UserService()
        user = us.create(u'warlock', u'avatar29A@gmail.com', u'12345', u'ru', u'en', u'Boris', u'Glebov')

        print u'User: {0}'.format(user)

        print u'\ndone'