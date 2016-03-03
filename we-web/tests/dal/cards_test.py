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

        self.user1 = self.us.create(u'user1')


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

        self.assertEqual(self.cs.list(self.user1), [])


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

        user = self.us.create(u'warlock')
        group = self.gs.pick_up(user)

        native = u'собака'
        foreign = u'dog'

        card = self.cs.create(user, group, foreign, native)

        self.assertIsNotNone(card)

        card.set_lang(user.native_lng)

        self.assertEqual(card.text, u'собака')

        card.set_lang(user.foreign_lng)

        self.assertEqual(card.text, u'dog')

    def test_create_cards_and_groups(self):
        """
        Creates 100 cards and check what groups have been created.
        """

        self.clear_db()

        user = self.us.create(u'warlock')

        cards_amount = 100

        for i in range(0, cards_amount):
            group = self.gs.pick_up(user)
            card = self.cs.create(user, group, u'dog', u'собака')

            self.assertIsNotNone(card)
            self.assertEqual(group.name, u'Group #{0}'.format((i / config.CARDS_IN_GROUP_AMOUNT) + 1))
