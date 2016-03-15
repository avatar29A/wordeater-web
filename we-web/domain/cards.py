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

    @property
    def foreign(self):
        self.set_lang(self.user.foreign_lng)
        return self.text

    @foreign.setter
    def foreign(self, value):
        self.set_lang(self.user.foreign_lng)
        self.text = value

    @property
    def native(self):
        self.set_lang(self.user.native_lng)
        return self.text

    @native.setter
    def native(self, value):
        self.set_lang(self.user.native_lng)
        self.text = value

    i18n = ['text', 'context', 'transcription']
    default_values = {
        'create_date': datetime.datetime.now(),
        'is_studying': True,
        'is_done': False
    }
