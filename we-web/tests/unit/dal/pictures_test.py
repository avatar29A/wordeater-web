# coding=utf-8

from tests.test_base import BaseTest
from services.service_locator import ServiceLocator

__author__ = 'Glebov Boris'


class PictureTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

        self.ps = ServiceLocator.resolve(ServiceLocator.PICTURES)


class PictureGetTest(PictureTest):
    """
    Test all case for translate method
    """

    def test_get_doesnt_exists_picture(self):
        """
        Translate new word. Save in DB.

        1. Check that translate is true
        2. Checks that word preserved in DB
        :return:
        """
        self.clear_db()
        self.create_demo_session()

        picture = self.ps.get(u'dog')

        self.assertIsNone(picture)

    def test_get_picture(self):
        self.clear_db()
        self.create_demo_session()

        self.ps.add(u'dog', 'gif')
        entity = self.ps.get(u'dog')

        self.assertIsNotNone(entity)
        self.assertEqual(entity.fs.content, 'gif')
