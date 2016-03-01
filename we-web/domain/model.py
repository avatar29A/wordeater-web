# coding=utf-8
__author__ = 'Warlock'

import config
import enums

from mongokit import *
import datetime

db = Connection(u"{0}:{1}".format(config.DATABASE['host'], config.DATABASE['port']))


class BaseDocument(Document):
    __database__ = config.DATABASE['db_name']

    use_dot_notation = True
    use_autorefs = True

    @property
    def id(self):
        return self._id

    def get_collection(self):
        raise Exception("Not implementated")

    def drop(self):
        return db[self.__database__][self.__collection__].drop()

    def commit(self, is_save=True):
        self.validate()
        if is_save:
            self.save()

        return self


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

    @property
    def cards(self):
        return db.Card.find({"user.$id": self.id})

    indexes = [
        {
            'fields': ['login'],
            'unique': True
        }]


@db.register
class Group(BaseDocument):
    __collection__ = "groups"

    structure = {
        'user': User,
        'name': unicode,
        'description': unicode,
        'cards_count': int,
        'cards_studying_count': int,
        'create_date': datetime.datetime
    }

    default_values = {
        'create_date': datetime.datetime.now(),
        'cards_count': 0,
        'cards_studying_count': 0
    }

    @property
    def cards(self):
        return db.Card.find({"group.$id": self.id})


@db.register
class Card(BaseDocument):
    __collection__ = "cards"

    structure = {
        # Ref
        'user': User,
        'group': Group,
        # Fields
        'text': unicode,
        'transcription': unicode,
        'context': unicode,
        'image_url': unicode,
        'is_studying': bool,
        'is_done': bool,
        'create_date': datetime.datetime
    }

    i18n = ['text', 'context', 'transcription']
    default_values = {
        'create_date': datetime.datetime.now(),
        'is_studying': True,
        'is_done': False
    }


@db.register
class Schedule(BaseDocument):
    __collection__ = "schedules"

    structure = {
        'user': User,
        'card': Card,
        'create_date': datetime.datetime,
        'dates': [{
            'date': datetime.datetime,
            'is_compleate': bool}]
    }

    default_values = {
        'create_date': datetime.datetime.now()
    }


@db.register
class ScheduleStatistic(BaseDocument):
    __collection__ = "schedule_statistics"

    structure = {
        'card': Card,
        'date': datetime.datetime,
        'type': IS(u'pass', u'done')
    }

    default_values = {
        'date': datetime.datetime.now()
    }


@db.register
class LoginAudit(BaseDocument):
    __collection__ = "login_audits"

    structure = {
        'login': unicode,
        'ip': unicode,
        'stamp': datetime.datetime
    }

