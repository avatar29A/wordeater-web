# coding=utf-8
from rest_test import *
import api.resources.cards.cards
from mongokit import ObjectId

__author__ = 'Glebov Boris'


class CardsGetTest(RestBaseTest):
    """
    Test all cases for method GET: /cards/
    """

    def test_get_empty(self):
        """
        Cards collection is empty
        :return: empty list
        """
        self.clear_db()
        self.create_demo_session()

        response_data = self._get()

        self.assertEqual(200, response_data[u'status'])
        self.assertEqual(response_data[u'data'], [])

    def test_get_one_card(self):
        """
        1. Create one card entity
        2. Send request on get all cards
        3. Check number received entities. Expected 1.
        """

        # Step 1
        self.clear_db()
        self.create_demo_session()

        us = ServiceLocator.resolve(ServiceLocator.USERS)
        gs = ServiceLocator.resolve(ServiceLocator.GROUPS)
        cs = ServiceLocator.resolve(ServiceLocator.CARDS)

        user = us.single(u'user1')
        group = gs.pick_up(user)
        cs.create(user, group, u'god', u'собака')

        # Step 2
        response_data = self._get()

        # Step 3
        self.assertEqual(200, response_data[u'status'])
        self.assertEqual(len(response_data[u'data']), 1)

    def _get(self):

        client_app = self.get_app_client()

        r = client_app.get('/api/v1/cards/')
        response_data = json.loads(r.data)

        return response_data


class CardsPostTest(RestBaseTest):
    """
    Test all cases for method POST: /cards/
    """

    def test_post_validation_fail(self):
        self.clear_db()
        self.create_demo_session()

        result_data = self._post({})

        self.assertEqual(result_data[u'status'], 4001)

    def test_create_new_card_fail_card_already_exists(self):
        """
        Checks case: 'Card already exists'
        :return:
        """
        self.clear_db()
        self.create_demo_session()

        us = ServiceLocator.resolve(ServiceLocator.USERS)
        cs = ServiceLocator.resolve(ServiceLocator.CARDS)
        gs = ServiceLocator.resolve(ServiceLocator.GROUPS)

        user = us.single(u'user1')
        group = gs.pick_up(user)

        cs.create(user, group, u'dog', u'собака')

        data = {
            u'foreign': u'dog',
            u'native': u'собака',
            u'context': u"dog it's human pet",
            u'transcription': u'',
        }

        result_data = self._post(data)

        self.assertEqual(result_data[u'status'], 409)

    def test_create_new_card(self):
        self.clear_db()
        self.create_demo_session()

        data = {
            u'foreign': u'dog',
            u'native': u'собака',
            u'context': u"dog it's human pet",
            u'transcription': u'',
        }

        result_data = self._post(data)

        self.assertEqual(result_data[u'status'], 201)
        self.assertEqual(result_data[u'data'][u'foreign'], data[u'foreign'])
        self.assertEqual(result_data[u'data'][u'native'], data[u'native'])
        self.assertEqual(result_data[u'data'][u'context'], u"dog it's human pet")

    def _post(self, data):
        client_app = self.get_app_client()

        r = client_app.post('/api/v1/cards/', headers=self.headers, data=json.dumps(data))
        response_data = json.loads(r.data)

        return response_data


class CardGetTest(RestBaseTest):
    """
    Checks all cases GET: /card/<card_id>/
    """

    def test_card_dont_exists(self):
        """
        Checks case when card don't exists

        1. Create new session
        2. Send request on GET:/card/<card.id>/
        3. Expected 404

        :return: 404
        """

        # Step 1
        self.clear_db()
        self.create_demo_session()

        # Step 2
        result = self._get(str(ObjectId()))

        # Step 3
        self.assertEqual(result[u'status'], 404)

    def test_card_exists(self):
        """
        Checks case when card exists

        1. Create new card
        2. Send request on GET:/card/<card.id>/
        3. Check response. Expected 200

        :return: 200
        """

        self.clear_db()
        self.create_demo_session()

        # Step 1
        us, gs, cs = _resolve_services()

        user = us.single(u'user1')
        group = gs.pick_up(user)

        card = cs.create(user, group, u'dog', u'собака')

        # Step 2
        result = self._get(str(card.id))

        # Step 3
        self.assertEqual(result[u'status'], 200)

    def _get(self, card_id):
        client_app = self.get_app_client()

        r = client_app.get('/api/v1/card/' + card_id + '/')
        response_data = json.loads(r.data)

        return response_data


class CardPutTest(RestBaseTest):
    """
    Checks all cases Post: /card/<card_id>/
    """

    def test_card_update_success(self):
        """
        1. Create new session
        2. Create new card from dal
        3. Try change native text. Send request on /card/<card.id>/
        4. Check card from dal
        :return:
        """

        # Step 1

        self.clear_db()
        self.create_demo_session()

        # Step 2
        us, gp, cs = _resolve_services()

        user = us.single(u'user1')
        group = gp.pick_up(user)

        card = cs.create(user, group, u'dog', u'собак')

        # Step 3
        data = {
            u'foreign': u'dog',
            u'native': u'собака'
        }

        r = self._patch(str(card.id), data)

        self.assertEqual(r[u'status'], 200)

        # Step 4
        changed_card = cs.single(user, u'dog', user.foreign_lng)
        self.assertEqual(changed_card.native, u'собака')

    def test_card_dupplicate_foreign(self):
        """
        1. Create new session
        2. Create two cards
        3. Try to change foreign card name. Set new foreign name as equal to second card. Send PATH request
        on /card/<card1.id>
        4. Expected status 409
        :return:
        """

        # Step 1

        self.clear_db()
        self.create_demo_session()

        # Step 2
        us, gp, cs = _resolve_services()

        user = us.single(u'user1')
        group = gp.pick_up(user)

        card1 = cs.create(user, group, u'dog', u'собака')
        card2 = cs.create(user, group, u'cat', u'кошка')

        # Step 3
        data = {
            u'foreign': u'cat',
            u'native': u'собака'
        }

        r = self._patch(str(card1.id), data)

        # Step 4

        self.assertEqual(r[u'status'], 409)

    def test_card_not_found(self):
        """
        1. Create new session
        2. Send request on /cards/<card.id>/ where card.id doesn't exists in DB
        3. Expeced 404

        :return: 404
        """

        # Step 1

        self.clear_db()
        self.create_demo_session()

        # Step 2

        data = {
            u'foreign': u'dog',
            u'native': u'собака'
        }

        r = self._patch(str(ObjectId()), data)

        # Step 3

        self.assertEqual(r[u'status'], 404)

    def _patch(self, card_id, data):
        client_app = self.get_app_client()

        r = client_app.patch('/api/v1/card/' + card_id + '/', headers=self.headers, data=json.dumps(data))
        response_data = json.loads(r.data)

        return response_data


def _resolve_services():
    us = ServiceLocator.resolve(ServiceLocator.USERS)
    gs = ServiceLocator.resolve(ServiceLocator.GROUPS)
    cs = ServiceLocator.resolve(ServiceLocator.CARDS)

    return us, gs, cs
