# coding=utf-8

from tests.test_base import BaseTest
from services.service_locator import ServiceLocator

__author__ = 'Glebov Boris'


class VoiceTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

        self.vs = ServiceLocator.resolve(ServiceLocator.VOICES)


class VoiceGetTest(VoiceTest):
    """
    Test all case for translate method
    """

    def test_get_doesnt_exists_voice(self):
        """
        Check to get voice from DB
        :return:
        """
        self.clear_db()
        self.create_demo_session()

        voice = self.vs.get(u'dog')

        self.assertIsNone(voice)

    def test_get_voice(self):
        self.clear_db()
        self.create_demo_session()

        self.vs.add(u'dog', 'wave')
        entity = self.vs.get(u'dog')

        self.assertIsNotNone(entity)
        self.assertEqual(entity.fs.content, 'wave')
