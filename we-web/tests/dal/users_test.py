# coding=utf-8

import unittest
from dal_test_base import db, BaseTest
from domain.users import User
from domain.cards import Card


__author__ = 'Glebov Boris'


class UsersTest(BaseTest):
    def test_user_create(self):
        user1 = User.create(u'user1')

        self.assertIsNotNone(user1, u"An user don't was created")
        self.assertEqual(user1.login, u'user1')

    def test_user_all(self):
        expected_user_amount = 2
        self._generate_users(expected_user_amount)

        self.assertEqual(len(User.all()), expected_user_amount)

    def test_user_single(self):
        self._generate_users(1)

        self.assertIsNotNone(User.single(u'user1'))

    def test_user_count(self):
        expected_user_amount = 2
        self._generate_users(expected_user_amount)

        self.assertEqual(expected_user_amount, User.count())

    def test_user_exists(self):
        self._generate_users(1)

        self.assertIsNotNone(User.exists(u'user1'))

    def test_user_cards(self):
        user1 = User.create(u'user1')

        self.assertEqual(user1.cards, [])

    def _generate_users(self, amount):
        for i in range(0, amount):
            User.create(u'user{0}'.format(i+1))
