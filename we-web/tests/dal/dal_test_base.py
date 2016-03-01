# coding=utf-8

import unittest
import config

from services.service_locator import ServiceLocator
from services.real.users import UserService

config.DATABASE['db_name'] = 'we_test'

from domain.model import db


class BaseTest(unittest.TestCase):
    def setUp(self):
        db.drop_database('we_test')

        ServiceLocator.register(ServiceLocator.DB, db)
        ServiceLocator.register(ServiceLocator.USERS, UserService())

    def tearDown(self):
        db.drop_database('we_test')
