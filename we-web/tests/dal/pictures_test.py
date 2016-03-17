# coding=utf-8

import unittest
from dal_test_base import BaseTest
from services.service_locator import ServiceLocator
from services.real.pictures import PictureService
from services.mocks.giphy import GiphyFake

__author__ = 'Glebov Boris'


class PictureTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

        self.ps = PictureService()
        self.ps.engine = GiphyFake()

        ServiceLocator.register(ServiceLocator.PICTURES, self.ps)


class PictureRandomTest(PictureTest):
    """
    Test all case for random method
    """

    def test_get_random_image(self):
        """
        Translate new word. Save in DB.

        1. Check that translate is true
        2. Checks that word preserved in DB
        """
        self.clear_db()
        self.create_demo_session()

        picture = self.ps.random(u'dog')

        self.assertIsNotNone(picture)

    def test_get_same_image(self):
        """
        1. Create session
        2. Create two random images
        3. Expected same id
        """

        self.clear_db()
        self.create_demo_session()

        picture1 = self.ps.random(u'dog')
        picture2 = self.ps.random(u'dog')

        self.assertEqual(picture1.id, picture2.id)
