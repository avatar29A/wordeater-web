# coding=utf-8

import config
from mongokit import ObjectId
from tests.test_base import BaseTest
from services.service_locator import ServiceLocator


__author__ = 'Glebov Boris'


class CardsTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

        self.cs = ServiceLocator.resolve(ServiceLocator.CARDS)
        self.us = ServiceLocator.resolve(ServiceLocator.USERS)
        self.gs = ServiceLocator.resolve(ServiceLocator.GROUPS)

    def _create_card(self, foreign, native):
        user = self.us.create(u'user1', u'user1@example.ru', u'qwerty')
        group = self.gs.pick_up(user)

        card = self.cs.create(user, group, foreign, native)

        return card


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


class CardsExtractTextTest(CardsTest):
    """
    Extract native and foreign text from card
    """

    def test_to_native(self):
        card = self._create_card(u'dog', u'собака')

        native = card.native

        self.assertEqual(u'собака', native)

    def test_to_foreign(self):
        card = self._create_card(u'dog', u'собака')

        foreign = card.foreign

        self.assertEqual(u'dog', foreign)


class CardsExistsTest(CardsTest):
    """
    Checks single and exists methods
    """

    def test_try_get_not_exists_card(self):
        """
        Try get not exists card.
        :return: None
        """
        self.clear_db()
        user = self.us.create(u'user1', u'user1@example.com', u'123')

        card = self.cs.single(user, u'dog', user.native_lng)

        self.assertEqual(card, None)

    def test_try_get_exists_card(self):
        """
        Try get exists card.
        :return: None
        """
        self.clear_db()

        card = self._create_card(u'dog', u'собака')
        user = card.user

        card = self.cs.single(user, card.native, card.user.native_lng)

        self.assertIsNotNone(card)

    def test_try_get_exists_card_by_id(self):
        """
        Try get exists card by Card ID
        :return: Card
        """
        self.clear_db()

        new_card = self._create_card(u'dog', u'собака')

        found_card = self.cs.get(new_card.user, new_card.id)

        self.assertIsNotNone(found_card)

    def test_try_get_dont_exists_card_by_id(self):
        """
        Try get don't exists card by Card ID
        :return: None
        """
        self.clear_db()
        user = self.us.create(u'user1', u'user1@example.com', u'123')

        found_card = self.cs.get(user, ObjectId())

        self.assertIsNone(found_card)

    def test_not_exists_card(self):
        """
        Checks what card don't exists
        :return: False
        """
        self.clear_db()

        user = self.us.create(u'user1', u'user1@example.com', u'123')

        result = self.cs.exists(user, u'dog', user.native_lng)

        self.assertEqual(result, False)

    def test_exists_card(self):
        """
        Checks what card is exists
        :return: True
        """
        self.clear_db()

        card = self._create_card(u'dog', u'собака')
        user = card.user

        result = self.cs.exists(user, card.native, card.user.native_lng)

        self.assertEqual(result, True)


