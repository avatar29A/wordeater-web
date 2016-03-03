# coding=utf-8

import config
import logger
import enums
import datetime

from mongokit import *

__author__ = 'Glebov Boris'


db = Connection(u"{0}:{1}".format(config.DATABASE['host'], config.DATABASE['port']))


class BaseDocument(Document):
    __database__ = config.DATABASE['db_name']

    use_dot_notation = True
    use_autorefs = True

    @property
    def id(self):
        return self._id

    def count(self):
        return db[self.__database__][self.__collection__].find().count()

    def all(self):
        return list(db[self.__database__][self.__collection__].find())

    def drop(self):
        return db[self.__database__][self.__collection__].drop()

    def commit(self, is_save=True):
        self.validate()
        if is_save:
            self.save()

        return self

#
# IMPORT MODELS

from domain.users import User
from domain.cards import Card
from domain.cards import Group
