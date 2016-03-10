# coding=utf-8

import unittest
import config
from dal_test_base import db, BaseTest
from services.service_locator import ServiceLocator


__author__ = 'Glebov Boris'


class CardsTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

        self.cs = ServiceLocator.resolve(ServiceLocator.CARDS)
        self.us = ServiceLocator.resolve(ServiceLocator.USERS)
        self.gs = ServiceLocator.resolve(ServiceLocator.GROUPS)


class CardsListTest(CardsTest):
    """
     Test all case for invoke of method 'list'
    """

    def test_list_without_user(self):
        """
        Returns list of card
        :return: throw AssertError exception
        """

        self.assertRaises(AssertionError, self.cs.list, None)

    def test_list_empty(self):
        """
        Returns list of card
        :return: list of card
        """

        self.clear_db()

        user = self.us.create(u'warlock', u'warlock@example.ru', u'qwerty')
        self.assertEqual(self.cs.list(user), [])


class CardsCreateTest(CardsTest):
    """
    Test all case for invoke of method 'create'
    """

    def test_create_contract(self):
        """
        Check contracts for methods
        :return: throw AssertError exception
        """

        self.assertRaises(AssertionError, self.cs.create, None, None, u'', u'')

    def test_create_card_dog(self):
        """
        Creates card with word is dog.
        :return: Card
        """
        self.clear_db()

        user = self.us.create(u'warlock', u'warlock@example.ru', u'qwerty')
        group = self.gs.pick_up(user)

        card = self.cs.create(user, group, u'dog', u'native')

        self.assertIsNotNone(card)

    def test_create_cards_and_groups(self):
        """
        Creates 100 cards and check what groups have been created.
        """

        self.clear_db()

        user = self.us.create(u'warlock', u'warlock@example.ru', u'qwerty')

        cards_amount = 100

        for i in range(0, cards_amount):
            group = self.gs.pick_up(user)
            card = self.cs.create(user, group, u'dog', u'собака')

            self.assertIsNotNone(card)
            self.assertEqual(group.name, u'Group #{0}'.format((i / config.CARDS_IN_GROUP_AMOUNT) + 1))


class CardsExtractText(CardsTest):
    """
    Extract native and foreign text from card
    """

    def test_to_native(self):
        card = self._create_card(u'dog', u'собака')

        native = self.cs.to_native(card)

        self.assertEqual(u'собака', native)

    def test_to_foreign(self):
        card = self._create_card(u'dog', u'собака')

        foreign = self.cs.to_foreign(card)

        self.assertEqual(u'dog', foreign)

    def _create_card(self, foreign, native):
        user = self.us.create(u'warlock', u'warlock@example.ru', u'qwerty')
        group = self.gs.pick_up(user)

        card = self.cs.create(user, group, foreign, native)

        return card

