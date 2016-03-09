# coding=utf-8

import config
import logger
import enums
import datetime
from utils.session_manager import UserSession
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

    def get_collection(self):
        return db[self.__database__][self.__collection__]

    @property
    def owner(self):
        return db.User.find_one({'_id': self.author})

    def count(self):
        return db[self.__database__][self.__collection__].find().count()

    def all(self):
        return list(db[self.__database__][self.__collection__].find())

    def drop(self):
        return db[self.__database__][self.__collection__].drop()

    def commit(self, is_save=True):
        user_session = UserSession.create()

        # Осуществляет защиту от подделки записи. Когда клиент может изменить
        # чужую запись:
        entity_id = self.id
        if entity_id:
            collection = self.get_collection()

            # Если id заполнен, нужно найти сущность:
            entity = collection.find_one({'_id': self.id})

            if entity is None:
                raise Exception("Action 'commit' raise excepton: Permission denided")

            # Если пользвоатель не админ, то авторство записи должно быть за ним
            if entity['author'] != user_session.id and not user_session.is_admin:
                raise Exception("Action 'commit' raise excepton: Permission denided")

            self.author = entity['author']
        else:
            if 'author' not in self or self.author is None:
                self.author = user_session.id

        self.validate()
        if is_save:
            self.save()

        return self

#
# IMPORT MODELS

from domain.users import User
from domain.cards import Card
from domain.cards import Group
from domain.login_audit import LoginAudit
from domain.schedules import Schedule
