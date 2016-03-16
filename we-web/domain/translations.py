# coding=utf-8

from model import *


@db.register
class Translation(BaseDocument):
    """
    Store all translations
    """

    __collection__ = "translations"

    structure = {
        'text': unicode,
        'foreign': unicode,
        'native': unicode,
        'author': unicode
    }

    required_fields = ['text', 'foreign', 'native']
    default_values = {
        'create_date': datetime.datetime.now(),
        'author': 'anonymous'
    }

    indexes = [
        {
            'fields': ['user', 'foreign', 'native'],
            'unique': True
        },
        {
            'fields': ['author']
        }]
