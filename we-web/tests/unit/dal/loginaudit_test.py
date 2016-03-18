# coding=utf-8

from tests.test_base import BaseTest
from services.service_locator import ServiceLocator

__author__ = 'Glebov Boris'


class LoginAuditsTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

        self.la_service = ServiceLocator.resolve(ServiceLocator.LOGIN_AUDIT)


class LoginAuditsCreateTest(LoginAuditsTest):
    def test_create_with_empty_args(self):
        """
        Pass emtpy args
        :return: throw AssertError exception
        """

        self.assertRaises(AssertionError, self.la_service.create, None, None)
        self.assertRaises(AssertionError, self.la_service.create, u'', u'')
