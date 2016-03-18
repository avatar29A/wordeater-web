# coding=utf-8

from tests.test_base import BaseTest
from services.service_locator import ServiceLocator

__author__ = 'Glebov Boris'


class GiphyTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

        self.gs = ServiceLocator.resolve(ServiceLocator.GIPHY)


class GiphyRandomTest(GiphyTest):
    """
    Test all case for random method
    """

    def test_get_random_image(self):
        """
        Get image from external service giphy.com
        """
        picture = self.gs.random(u'dog')

        self.assertIsNotNone(picture)
