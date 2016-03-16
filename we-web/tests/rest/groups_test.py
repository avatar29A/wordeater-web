# coding=utf-8

from rest_test import *
import api.resources.groups.groups
from mongokit import ObjectId

__author__ = 'Glebov Boris'


class GroupsGetAPI(RestBaseTest):
    """
    Test all cases for method GET: /cards/
    """

    def test_get_empty(self):
        """
        Groups collection is empty
        :return: empty list
        """
        self.clear_db()
        self.create_demo_session()

        response_data = self._get()

        self.assertEqual(200, response_data[u'status'])
        self.assertEqual(response_data[u'data'], [])

    def test_get_one_group(self):
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

        user = us.single(u'user1')
        group = gs.create(user, u'group1', u'group1')

        # Step 2
        response_data = self._get()

        # Step 3
        self.assertEqual(200, response_data[u'status'])
        self.assertEqual(len(response_data[u'data']), 1)

    def _get(self):

        client_app = self.get_app_client()

        r = client_app.get('/api/v1/groups/')
        response_data = json.loads(r.data)

        return response_data


class GroupsPostAPI(RestBaseTest):
    """
    Test all cases for method POST: /cards/
    """

    def test_post_validation_fail(self):
        """
        1.
        """
        self.clear_db()
        self.create_demo_session()

        result_data = self._post({})

        self.assertEqual(result_data[u'status'], 4001)

    def test_create_new_group_fail_group_already_exists(self):
        """
        1. Create new session
        2. Create one group
        3. Send request on create group yet
        4. Expected 409
        :return:
        """
        # Step 1
        self.clear_db()
        self.create_demo_session()

        us = ServiceLocator.resolve(ServiceLocator.USERS)
        gs = ServiceLocator.resolve(ServiceLocator.GROUPS)

        # Step 2
        user = us.single(u'user1')
        group = gs.create(user, u'group1', u'')

        # Step 3
        data = {
            u'name': u'group1',
            u'description': u''
        }

        result_data = self._post(data)

        # Step 4
        self.assertEqual(result_data[u'status'], 409)

    def test_create_new_group(self):
        """
        1. Create new session
        2. Send request for create new group on POST:/api/v1/groups/
        3. Expected 201
        4. Check through DAL, that group was created.
        """

        # Step 1
        self.clear_db()
        self.create_demo_session()

        us = ServiceLocator.resolve(ServiceLocator.USERS)
        gs = ServiceLocator.resolve(ServiceLocator.GROUPS)

        user = us.single(u'user1')

        # Step 2
        data = {
            u'name': u'group1',
            u'description': u''
        }

        response_data = self._post(data)

        # Step 3
        self.assertEqual(201, response_data[u'status'])

        # Step 4
        group = gs.single(user=user, name=u'group1')

        self.assertIsNotNone(group)

    def _post(self, data):
        client_app = self.get_app_client()

        r = client_app.post('/api/v1/groups/', headers=self.headers, data=json.dumps(data))
        response_data = json.loads(r.data)

        return response_data


class GroupGetAPI(RestBaseTest):
    """
    Test all cases for method GET: /card/<group_id>/
    """

    def test_get_empty(self):
        """
        1. Create session
        2. Send request with ID. This ID doesn't exists.
        3. Expected 404
        """
        # Step 1
        self.clear_db()
        self.create_demo_session()

        # Step 2
        response_data = self._get(str(ObjectId()))

        # Step 3
        self.assertEqual(404, response_data[u'status'])

    def test_get_group_without_cards(self):
        """
        1. Create session
        2. Create new empty group
        3. Send request with ID. This ID exists in DB
        4. Expected 200
        5. Check response
        """

        # Step 1
        self.clear_db()
        self.create_demo_session()

        # Step 2
        us = ServiceLocator.resolve(ServiceLocator.USERS)
        gs = ServiceLocator.resolve(ServiceLocator.GROUPS)

        user = us.single(u'user1')
        group = gs.create(user, u'group1', u'')

        # Step 3
        response_data = self._get(str(group.id))

        # Step 4
        self.assertEqual(200, response_data[u'status'])
        self.assertEqual(u'group1', response_data[u'data'][u'name'])

    def test_get_group_with_cards(self):
        """
        1. Create session
        2. Create new group
        3. Add some cards to group
        4. Send GET request
        5. Expected 200
        6. Check response
        :return:
        """

        # Step 1
        self.clear_db()
        self.create_demo_session()

        # Step 2
        us = ServiceLocator.resolve(ServiceLocator.USERS)
        gs = ServiceLocator.resolve(ServiceLocator.GROUPS)
        cs = ServiceLocator.resolve(ServiceLocator.CARDS)

        user = us.single(u'user1')
        group = gs.create(user, u'group1', u'')

        # Step 3
        card1 = cs.create(user, group, u'dog', u'собака')
        card2 = cs.create(user, group, u'cat', u'кошка')

        # Step 4
        response_data = self._get(str(group.id))

        # Step 5
        self.assertEqual(200, response_data[u'status'])

        # Step 6
        self.assertEqual(u'group1', response_data[u'data'][u'name'])
        self.assertEqual(2, len(response_data[u'data'][u'cards']))

    def _get(self, group_id):
        client_app = self.get_app_client()

        r = client_app.get('/api/v1/group/' + group_id + '/')
        response_data = json.loads(r.data)

        return response_data


class GroupPatchAPI(RestBaseTest):
    """
    Test all cases for method PATCH: /card/<group_id>/
    """

    def test_try_patch_doesnt_exists_group(self):
        """
        1. Create sessions
        2. Send request with fake ID
        3. Expected 404
        """

        # Step 1
        self.clear_db()
        self.create_demo_session()

        # Step 2
        data = {u'name': u'group2'}

        response_data = self._patch(str(ObjectId()), data)

        # Step 3
        self.assertEqual(404, response_data[u'status'])

    def test_duplicate_group_name(self):
        """
        1. Create sessions
        2. Create two group: group1 and group2
        3. Try change name the first group on the group2 through API
        4. Expected 409
        """
        # Step 1
        self.clear_db()
        self.create_demo_session()

        # Step 2
        us = ServiceLocator.resolve(ServiceLocator.USERS)
        gs = ServiceLocator.resolve(ServiceLocator.GROUPS)

        user = us.single(u'user1')

        group1 = gs.create(user, u'group1', u'')
        group2 = gs.create(user, u'group2', u'')

        # Step 3
        data = {u'name': u'group2'}

        response_data = self._patch(str(group1.id), data)

        # Step 4
        self.assertEqual(409, response_data[u'status'])

    def test_patch_success(self):
        """
        1. Create sessions
        2. Create one group
        3. Try change group name
        4. Expected 200
        5. Check through DAL, a new group name.
        """
        # Step 1
        self.clear_db()
        self.create_demo_session()

        # Step 2
        us = ServiceLocator.resolve(ServiceLocator.USERS)
        gs = ServiceLocator.resolve(ServiceLocator.GROUPS)

        user = us.single(u'user1')

        group1 = gs.create(user, u'group1', u'')

        # Step 3
        data = {u'name': u'group2'}

        response_data = self._patch(str(group1.id), data)

        # Step 4
        self.assertEqual(200, response_data[u'status'])

        # Step 5
        group2 = gs.single(user=user, name=u'group2')
        self.assertIsNotNone(group2, u"Group with name 'group2' doesn't found")

    def _patch(self, group_id, data):
        client_app = self.get_app_client()

        r = client_app.patch('/api/v1/group/' + group_id + '/', headers=self.headers, data=json.dumps(data))
        response_data = json.loads(r.data)

        return response_data
