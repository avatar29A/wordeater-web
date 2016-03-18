# coding=utf-8

from model import *


@db.register
class Voice(BaseDocument):
    """
    Store all voices
    """

    __collection__ = "voices"

    structure = {
        "text": unicode,
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
        }]

    gridfs = {
        'files': ['source'],
        'containers': ['voices']
    }
