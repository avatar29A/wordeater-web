# coding=utf-8

import unittest
import config

config.DATABASE['db_name'] = 'we_test'

from domain.model import db


class BaseTest(unittest.TestCase):
    def setUp(self):
        db.drop_database('we_test')

    def tearDown(self):
        db.drop_database('we_test')
