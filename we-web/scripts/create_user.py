# coding=utf-8
__author__ = 'Warlock'

from flask.ext.script import Command
from services.users import UserService
from domain.model import db


class CreateUser(Command):
    """
    Add new user with name Warlock
    """

    def run(self):
        print u"Run create user with name 'warlock'"

        us = UserService(db)
        user = us.create(u'warlock', u'ru', u'en', u'Boris', u'Glebov')

        print u'User: {0}'.format(user)

        print u'\ndone'