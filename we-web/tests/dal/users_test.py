# coding=utf-8

from dal_test_base import BaseTest, ServiceLocator

__author__ = 'Glebov Boris'


class UsersTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

        self.us = ServiceLocator.resolve(ServiceLocator.USERS)

    def test_user_create(self):
        user1 = self.us.create(u'user1')

        self.assertIsNotNone(user1, u"An user don't was created")
        self.assertEqual(user1.login, u'user1')

    def test_user_single(self):
        self._generate_users(1)

        self.assertIsNotNone(self.us.single(u'user1'))

    def test_user_exists(self):
        self._generate_users(1)

        self.assertIsNotNone(self.us.exists(u'user1'))

    def test_user_cards(self):
        user1 = self.us.create(u'user1')

        self.assertEqual(user1.cards, [])

    def _generate_users(self, amount):
        for i in range(0, amount):
            self.us.create(u'user{0}'.format(i+1))
