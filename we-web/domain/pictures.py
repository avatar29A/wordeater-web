# coding=utf-8

from model import *


@db.register
class Picture(BaseDocument):
    """
    Store all pictures
    """

    __collection__ = "pictures"

    structure = {
        'text': unicode,
        'author': unicode,
        'create_date': datetime.datetime
    }

    required_fields = ['text']
    default_values = {
        'create_date': datetime.datetime.now(),
        'author': 'anonymous'
    }

    indexes = [
        {
            'fields': ['text'],
            'unique': True
        },
        {
            'fields': ['author']
        }]

    gridfs = {
        'files': ['content'],
        'containers': ['pictures']
    }
