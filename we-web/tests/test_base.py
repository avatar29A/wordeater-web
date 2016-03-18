# coding=utf-8

import unittest
import config

# REAL
from services.service_locator import ServiceLocator
from services.real.users import UserService
from services.real.groups import GroupService
from services.real.cards import CardService
from services.real.login_audits import LoginAutits
from services.real.schedules import ScheduleService
from services.real.translate import TranslateService
from services.real.pictures import PictureService
from services.real.voices import VoicesService

# MOCKS
from services.mocks.session import SessionService
from services.mocks.vocabularity import VocabularityService
from services.mocks.yandex_translate import YandexTranslateFake
from services.mocks.giphy import GiphyFake
from services.mocks.bluemix import BluemixFake

config.DATABASE['db_name'] = 'we_test'
config.IS_DEBUG = True

# Database must be under define config.DATABASE['db_name'] = 'we_test'
from domain.model import db


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.clear_db()

        self.headers = [('Content-Type', 'application/json')]

        ServiceLocator.register(ServiceLocator.DB, db)
        ServiceLocator.register(ServiceLocator.USERS, UserService())
        ServiceLocator.register(ServiceLocator.GROUPS, GroupService())
        ServiceLocator.register(ServiceLocator.CARDS, CardService())
        ServiceLocator.register(ServiceLocator.LOGIN_AUDIT, LoginAutits())
        ServiceLocator.register(ServiceLocator.SCHEDULES, ScheduleService())
        ServiceLocator.register(ServiceLocator.PICTURES, PictureService())
        ServiceLocator.register(ServiceLocator.VOICES, VoicesService())

        # Mock:
        ServiceLocator.register(ServiceLocator.SESSIONS, SessionService())
        ServiceLocator.register(ServiceLocator.VOCABULARITY, VocabularityService())
        ServiceLocator.register(ServiceLocator.GIPHY, GiphyFake())
        ServiceLocator.register(ServiceLocator.BLUEMIX, BluemixFake())

        # Mock translate service
        ts = TranslateService()
        ts.engine = YandexTranslateFake()
        ServiceLocator.register(ServiceLocator.TRANSLATIONS, ts)

    def create_demo_user(self):
        us = ServiceLocator.resolve(ServiceLocator.USERS)

        user = us.create(u'user1', u'user1@mail.ru', u'12345')

        return user

    def create_demo_session(self):
        us = ServiceLocator.resolve(ServiceLocator.USERS)
        ss = ServiceLocator.resolve(ServiceLocator.SESSIONS)

        user = self.create_demo_user()
        token = us.make_auth_token(user)

        return ss.create(user, token)

    def tearDown(self):
        self.clear_db()

    def clear_db(self):
        db.drop_database('we_test')
