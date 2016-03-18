# coding=utf-8

from tests.test_base import BaseTest
from services.service_locator import ServiceLocator


__author__ = 'Glebov Boris'


class BluemixTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

        self.bs = ServiceLocator.resolve(ServiceLocator.BLUEMIX)


class BluemixSynthTest(BluemixTest):
    def test_synth_text(self):
        """
        Test that service will return synthesized text.
        :return: synthesized text
        """

        content = self.bs.synthesize("Hello world!")

        self.assertIsNotNone(content)
