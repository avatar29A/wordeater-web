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

