# coding=utf-8

from model import *
from users import User

__author__ = 'Glebov Boris'


@db.register
class Group(BaseDocument):
    """
    Description group entity
    """
    __collection__ = "groups"

    structure = {
        'user': User,
        'name': unicode,
        'description': unicode,
        'cards_count': int,
        'cards_studying_count': int,
        'create_date': datetime.datetime,
        'author': ObjectId
    }

    default_values = {
        'create_date': datetime.datetime.now(),
        'cards_count': 0,
        'cards_studying_count': 0
    }

    @property
    def cards(self):
        return db.Card.find({"group.$id": self.id})
