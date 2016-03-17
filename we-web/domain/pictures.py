# coding=utf-8

from model import *


@db.register
class Picture(BaseDocument):
    """
    Storee all pictures
    """

    __collection__ = "pictures"

    structure = {
        'text': unicode,
        'mp4': unicode,
        'url': unicode,
        'original': unicode,
        'original_small': unicode,
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
        'files':['source'],
        'containers': ['images']
    }
