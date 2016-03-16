# coding=utf-8
from model import *
from users import User
from cards import Card


@db.register
class Schedule(BaseDocument):
    __collection__ = "schedules"

    structure = {
        'user': User,
        'card': Card,
        'create_date': datetime.datetime,
        'dates': [{
            'date': datetime.datetime,
            'is_compleate': bool}],
        'author': ObjectId
    }

    required_fields = ['user', 'card']
    indexes = [{
        'fields': ['user', 'card'],
        'unique': True
    }]

    default_values = {
        'create_date': datetime.datetime.now()
    }
