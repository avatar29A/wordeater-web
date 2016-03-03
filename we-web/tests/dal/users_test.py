# coding=utf-8

from dal_test_base import BaseTest, ServiceLocator

__author__ = 'Glebov Boris'


class UsersTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

        self.us = ServiceLocator.resolve(ServiceLocator.USERS)

    def _generate_users(self, amount):
        for i in range(0, amount):
            self.us.create(u'user{0}'.format(i+1))


class UsersCreateTest(UsersTest):
    """
    Test all case for 'create' method
    """

    def test_create_without_login(self):
        """
        Invokes 'create' method without login.
        :return: throw AssertError exception
        """

        self.assertRaises(AssertionError, self.us.create, None)
        self.assertRaises(AssertionError, self.us.create, u'')

    def test_user_create(self):
        """

        :return:
        """
        user1 = self.us.create(u'user1')

        self.assertIsNotNone(user1, u"An user don't was created")
        self.assertEqual(user1.login, u'user1')


class UsersSingleTest(UsersTest):
    """
    Test all case for 'single' method
    """

    def test_single_without_login(self):
        """
        Invokes 'single' method without login.
        :return: throw AssertError exception
        """

        self.assertRaises(AssertionError, self.us.single, None)
        self.assertRaises(AssertionError, self.us.single, u'')

    def test_find_no_exists_user(self):
        """
        Tries to find user which don't exists
        :return: None
        """
        user = self.us.single(u'no_exists_user_login')

        self.assertIsNone(user)

    def test_find_exists_user(self):
        """
        Tries to find exists user
        :return:
        """

        login = u'user_0000100'
        self.us.create(login)

        self.assertIsNotNone(self.us.single(login))
        self.assertEqual(self.us.single(login).login, login)

    def test_user_exists(self):
        """
        Check on user is exists
        :return: Boolean. True if user is exists.
        """
        self._generate_users(1)

        self.assertIsNotNone(self.us.exists(u'user1'))
