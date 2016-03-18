# coding=utf-8

import os
from tests.test_base import BaseTest
from services.external.giphy import GiphyService

__author__ = 'Glebov Boris'


class GiphyTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

        self.gs = GiphyService()


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
