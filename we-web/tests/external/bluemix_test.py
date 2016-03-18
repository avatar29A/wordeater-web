# coding=utf-8

from tests.test_base import BaseTest
from services.external.bluemix import BluemixService


__author__ = 'Glebov Boris'


class BluemixTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

        self.bs = BluemixService()


class BluemixSynthTest(BluemixTest):
    def test_synth_text(self):
        """
        Test that service will return synthesized text.
        :return: synthesized text
        """

        content = self.bs.synthesize("Hello world!")

        self.assertIsNotNone(content)
