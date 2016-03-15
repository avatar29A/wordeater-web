# coding=utf-8

from rest_test import *
import api.resources.users.users

__author__ = 'Glebov Boris'


class UserListTest(RestBaseTest):
    """
    Test all case for GET: /api/v1/users/
    """
    def test_users_list_success(self):
        client_app = self.get_app_client()

        r = client_app.get('/api/v1/users/')
        data = json.loads(r.data)

        self.assertEqual(data[u'status'], 200)


class UserSignInTest(RestBaseTest):
    """
    Test all case for POST: /api/v1/users/signin/
    """

    def test_users_signin_fail(self):
        """
        Check what:
         1. User's login not found,
         OR
         2. Password is incorrect
        """
        client_app = self.get_app_client()

        data = {
            u'login': u'123',
            u'password': u'123'
        }

        r = client_app.post('/api/v1/user/signin/', headers=self.headers, data=json.dumps(data))
        response_data = json.loads(r.data)

        self.assertEqual(4001, response_data[u'status'])

    def test_users_signin_ok(self):
        """
        Check what:
         1. Users with login is exists
         2. Password is correct
        """

        us = ServiceLocator.resolve(ServiceLocator.USERS)
        us.create(u'user1', u'user1@example.com', u'123', first_name=u'demo', last_name=u'demo')

        client_app = self.get_app_client()

        data = {
            u'login': u'user1',
            u'password': u'123'
        }

        r = client_app.post('/api/v1/user/signin/', headers=self.headers, data=json.dumps(data))
        response_data = json.loads(r.data)

        self.assertEqual(response_data[u'status'], 200)
        self.assertIsNotNone(response_data[u'data'][u'auth_token'])


class UserSignUpTest(RestBaseTest):
    """
    Test all case for POST: /api/v1/users/signup/
    """

    def test_users_signup_fail_email_is_exists(self):
        """
        Checks what we normal handled next cases:
         1. Email is exists
        """

        self.clear_db()

        us = ServiceLocator.resolve(ServiceLocator.USERS)
        us.create(u'user1', u'user1@example.com', u'123', first_name=u'demo', last_name=u'demo')

        client_app = self.get_app_client()

        data = {
            u'login': u'user1',
            u'email': u'user222@example.com',
            u'password': u'123',
            u'first_name': u'aa',
            u'last_name': u'aa'
        }

        r = client_app.post('/api/v1/user/signup/', headers=self.headers, data=json.dumps(data))
        response_data = json.loads(r.data)

        self.assertEqual(response_data[u'status'], 4001)
        self.assertEqual(response_data[u'errors'][u'error_type'], u'user_already_exists_error', u'Login already exists')

    def test_users_signup_fail_login_is_exists(self):
        """
        Checks what we normal handled next cases:
         1. Login is exists
        """

        self.clear_db()

        us = ServiceLocator.resolve(ServiceLocator.USERS)
        us.create(u'user1', u'user1@example.com', u'123', first_name=u'demo', last_name=u'demo')

        client_app = self.get_app_client()

        data = {
            u'login': u'user2',
            u'email': u'user1@example.com',
            u'password': u'123',
            u'first_name': u'aa',
            u'last_name': u'aa'
        }

        r = client_app.post('/api/v1/user/signup/', headers=self.headers, data=json.dumps(data))
        response_data = json.loads(r.data)

        self.assertEqual(response_data[u'status'], 4001)
        self.assertEqual(response_data[u'errors'][u'error_type'], u'email_already_exists', u'Email already exists')

    def test_users_signup_ok(self):
        """
        User signup is successfully
        :return:
        """

        self.clear_db()

        client_app = self.get_app_client()

        data = {
            u'login': u'user1',
            u'email': u'user1@example.com',
            u'password': u'123',
            u'first_name': u'aa',
            u'last_name': u'aa'
        }

        r = client_app.post('/api/v1/user/signup/', headers=self.headers, data=json.dumps(data))
        response_data = json.loads(r.data)

        self.assertEqual(response_data[u'status'], 201)

        us = ServiceLocator.resolve(ServiceLocator.USERS)
        user = us.single(u'user1')

        self.assertIsNotNone(user)


class UserCheckTest(RestBaseTest):
    """
    Test all case for POST: /api/v1/users/check/
    """

    def test_user_check_login_is_exists(self):
        """
        Test case:
            Login is exists
        """
        data = {
            u'login': u'user1',
        }

        response_data = self._test_check(data)

        self.assertEqual(response_data[u'status'], 200)
        self.assertEqual(response_data[u'data'][u'login'], False)

    def test_user_check_email_is_exists(self):
        """
        Test case:
            Email is exists
        """
        data = {
            u'email': u'user1@example.com',
        }

        response_data = self._test_check(data)

        self.assertEqual(response_data[u'status'], 200)
        self.assertEqual(response_data[u'data'][u'email'], False)

    def test_user_check_login_ok(self):
        """
        Test case:
            Login is not exists
        """
        data = {
            u'login': u'user2'
        }

        response_data = self._test_check(data)

        self.assertEqual(response_data[u'status'], 200)
        self.assertEqual(response_data[u'data'][u'login'], True)

    def test_user_check_email_ok(self):
        """
        Test case:
            Email is not exists
        """
        data = {
            u'email': u'user2@example.com'
        }

        response_data = self._test_check(data)

        self.assertEqual(response_data[u'status'], 200)
        self.assertEqual(response_data[u'data'][u'email'], True)

    def test_user_check_login_email_ok(self):
        """
        Test case:
            Login and Email is not exists
        """
        data = {
            u'login': u'user2',
            u'email': u'user2@example.com'
        }

        response_data = self._test_check(data)

        self.assertEqual(response_data[u'status'], 200)
        self.assertEqual(response_data[u'data'][u'login'], True)
        self.assertEqual(response_data[u'data'][u'email'], True)

    def test_user_check_login_email_fail(self):
        """
        Test case:
            Login and Email is not exists
        """
        data = {
            u'login': u'user1',
            u'email': u'user1@example.com'
        }

        response_data = self._test_check(data)

        self.assertEqual(response_data[u'status'], 200)
        self.assertEqual(response_data[u'data'][u'login'], False)
        self.assertEqual(response_data[u'data'][u'email'], False)

    def test_user_check_login_email_none(self):
        """
        Test case:
            Login and Email didn't send
        """
        data = {

        }

        response_data = self._test_check(data)

        self.assertEqual(response_data[u'status'], 200)
        self.assertEqual(response_data[u'data'][u'login'], None)
        self.assertEqual(response_data[u'data'][u'email'], None)

    def _test_check(self, data):
        self.clear_db()

        us = ServiceLocator.resolve(ServiceLocator.USERS)
        us.create(u'user1', u'user1@example.com', u'123', first_name=u'demo', last_name=u'demo')

        client_app = self.get_app_client()

        r = client_app.post('/api/v1/users/check/', headers=self.headers, data=json.dumps(data))
        response_data = json.loads(r.data)

        return response_data
