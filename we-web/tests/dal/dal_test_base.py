# coding=utf-8

import unittest
import config

from services.service_locator import ServiceLocator
from services.real.users import UserService
from services.real.groups import GroupService
from services.real.cards import CardService
from services.real.login_audits import LoginAutits


config.DATABASE['db_name'] = 'we_test'

from domain.model import db


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.clear_db()

        ServiceLocator.register(ServiceLocator.DB, db)
        ServiceLocator.register(ServiceLocator.USERS, UserService())
        ServiceLocator.register(ServiceLocator.GROUPS, GroupService())
        ServiceLocator.register(ServiceLocator.CARDS, CardService())
        ServiceLocator.register(ServiceLocator.LOGIN_AUDIT, LoginAutits())

    def tearDown(self):
        self.clear_db()

    def clear_db(self):
        db.drop_database('we_test')
