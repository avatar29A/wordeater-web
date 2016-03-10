# coding=utf-8
from model import *


@db.register
class User(BaseDocument):
    __collection__ = "users"

    structure = {
        'login': unicode,
        'password': unicode,
        'email': unicode,

        'first_name': unicode,
        'last_name': unicode,

        'native_lng': IS(*enums.LANGUAGE),
        'foreign_lng': IS(*enums.LANGUAGE),

        'create_date': datetime.datetime,

        'advanced': {
            'birthday': datetime.datetime,
            'sex': IS(*enums.SEX),
        },

        'settings': {
           'is_active': bool,  # Пользователь активирован
           'activation_code': unicode,
           'is_reminders_turn': bool,  # Напоминания включены
           'is_notifications_turn': bool  # Уведомления включены
        }
    }

    required_fields = ['login', 'email', 'native_lng']

    default_values = {
        'create_date': datetime.datetime.now(),
        # Advanced
        'advanced.sex': u'male',
        # Settings
        'settings.is_active': False,
        'settings.is_reminders_turn': True,
        'settings.is_notifications_turn': True,
    }

    indexes = [
        {
            'fields': ['login', 'email', 'password', 'native_lng', 'foreign_lng'],
            'unique': True
        }]

    @property
    def cards(self):
        return list(db.Card.find({"user.$id": self.id}))

