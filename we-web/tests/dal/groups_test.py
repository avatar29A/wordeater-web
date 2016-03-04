# coding=utf-8

from dal_test_base import db, BaseTest
from services.service_locator import ServiceLocator

__author__ = 'Glebov Boris'


class GroupsTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

        self.gs = ServiceLocator.resolve(ServiceLocator.GROUPS)
        self.us = ServiceLocator.resolve(ServiceLocator.USERS)

    @property
    def user1(self):
        user = self.us.create(u'user1')
        return user

    def _generate_groups(self, user, amount):
        for i in range(0, amount):
            self.gs.create(user, u'Group {0}'.format(i+1))


class GroupListTest(GroupsTest):
    """
    Test all case for invoke of method 'list'
    """

    def test_list_without_user(self):
        """
        It must throw exception AssertError
        :return: AssertError
        """

        self.assertRaises(AssertionError, self.gs.list, None)

    def test_list_with_user(self):
        """
        Returns list of groups
        :return: List of groups
        """
        self._generate_groups(self.user1, 3)

        self.assertEqual(len(self.gs.list(self.user1)), 3)


class GroupSingleTest(GroupsTest):
    """
    Test all case for invoke of method 'single'
    """

    def test_empty_groupid(self):
        """
        It have to throw exception if no pass arguments.
        """
        self.assertRaises(AssertionError, self.gs.single)

    def test_get_group_by_id(self):
        """
        Get group by ID
        :return:
        """
        group = self.gs.create(self.user1, u'Group3')

        find_group = self.gs.single(group.id)

        self.assertIsNotNone(find_group)
        self.assertEqual(find_group.name, u'Group3')

    def test_get_group_by_name_fail(self):
        """
        Get group by Name. It must return None:
        :return: None
        """

        find_group = self.gs.single(user=self.user1, name=u'Group2')
        self.assertIsNone(find_group, u'It must return None')

    def test_get_group_by_name_ok(self):
        """
        Get group by Name. It must return Group:
        :return: Group entity
        """
        self.gs.create(self.user1, u'Group3')

        find_group = self.gs.single(user=self.user1, name=u'Group3')
        self.assertIsNotNone(find_group, u'It must return Group Entity')

    def test_get_group_by_user(self):
        """
        Returns a group where amount cards less than config.CARDS_IN_GROUP_AMOUNT
        :return: Group
        """

        group = self.gs.single(None, self.user1)

        self.assertIsNotNone(group, u"Returned value is shoudn't be None")


class GroupCreateTest(GroupsTest):
    """
    Test all case for invoke of method 'create' from GroupService
    """

    def test_try_create_without_user(self):
        """
        It must throw exception
        :return: AssertionError
        """
        self.assertRaises(AssertionError, self.gs.create, None, None)

    def test_try_create_without_name(self):
        """
        It must throw exception
        :return: AssertionError
        """
        self.assertRaises(AssertionError, self.gs.create, self.user1, u"")
        self.assertRaises(AssertionError, self.gs.create, self.user1, None)

    def test_try_create(self):
        """
        It must return Group entity
        :return: Group entity
        """
        group = self.gs.create(self.user1, u"Group3")
        self.assertIsNotNone(group, u"It can't be a None")


class GroupRenameTest(GroupsTest):
    """
    Test all case for invoke of method 'rename'
    """

    def test_rename_with_wrong_parameters(self):
        """
        Test empty input parameters
        :return: throw AssertError exception
        """

        # All parameters is None
        self.assertRaises(AssertionError, self.gs.rename, None, None, None)

        # name is empty string and new_name is None
        self.assertRaises(AssertionError, self.gs.rename, None, u'', None)

    def test_rename_not_exists_group(self):
        """
        Try rename don't exists group
        :return: None
        """

        self.assertIsNone(self.gs.rename(self.user1, u'group2', u'new_name'))

    def test_rename(self):
        """
        Try rename group
        :return: Group
        """

        old_name = u'group1'
        new_name = u'group2'

        self.gs.create(self.user1, old_name)

        rename_group = self.gs.rename(self.user1, old_name, new_name)

        self.assertIsNotNone(rename_group, u"Return value is None")
        self.assertEqual(rename_group.name, new_name)


class GroupCountTest(GroupsTest):
    """
    Test all case for invoke of method 'count'
    """

    def test_count_when_user_is_none(self):
        """
        Pass None in user argument
        :return: throw user
        """

        self.assertRaises(AssertionError, self.gs.count, None)

    def test_count_with_user(self):
        """
        Return count user's groups
        :return: Count user's groups
        """
        self._generate_groups(self.user1, 3)
        self.assertEqual(self.gs.count(self.user1), 3)
