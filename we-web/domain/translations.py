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
        'variations': [unicode],
        'direction': unicode,
        'author': unicode,
        'create_date': datetime.datetime
    }

    required_fields = ['text', 'direction']
    default_values = {
        'create_date': datetime.datetime.now(),
        'author': 'anonymous'
    }

    indexes = [
        {
            'fields': ['text', 'direction'],
            'unique': True
        },
        {
            'fields': ['author']
        }]
