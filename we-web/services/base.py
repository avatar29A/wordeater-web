# coding=utf-8
__author__ = 'Warlock'


class BaseService(object):
    def __init__(self, connection):
        self.connection = connection

    def _set_native(self, user, document):
        document.set_lang(user.native_lng)

    def _set_foreign(self, user, document):
        document.set_lang(user.foreign_lng)