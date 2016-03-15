# coding=utf-8

from model import *
from users import User
from groups import Group


@db.register
class Card(BaseDocument):
    """
    Card entity
    """
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
