# coding=utf-8
from model import *
from cards import Card


@db.register
class ScheduleStatistic(BaseDocument):
    __collection__ = "schedule_statistics"

    structure = {
        'card': Card,
        'date': datetime.datetime,
        'type': IS(u'pass', u'done'),
        'author': ObjectId
    }

    default_values = {
        'date': datetime.datetime.now()
    }

    @staticmethod
    def get_collection():
        return db.ScheduleStatistic
