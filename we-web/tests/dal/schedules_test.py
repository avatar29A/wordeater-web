# coding=utf-8

from dal_test_base import db, BaseTest
from services.service_locator import ServiceLocator
from pydash import py_
from datetime import datetime, date

__author__ = 'Glebov Boris'


class ScheduleTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

        self.us = ServiceLocator.resolve(ServiceLocator.USERS)
        self.cs = ServiceLocator.resolve(ServiceLocator.CARDS)
        self.gs = ServiceLocator.resolve(ServiceLocator.GROUPS)
        self.ss = ServiceLocator.resolve(ServiceLocator.SCHEDULES)

    def _create_test_user_and_card(self):
        user = self.us.create(u'user')
        group = self.gs.pick_up(user)
        card = self.cs.create(user, group, u'dog', u'собака')

        return user, card


class ScheduleSingleTest(ScheduleTest):
    """
    Test all case invoke 'single' method
    """

    def test_single_with_empty_args(self):
        """
        Invoke 'single' with empty args
        :return: throw AssertError exception
        """

        user, card = self._create_test_user_and_card()
        self.ss.create(user, card)

        self.assertIsNotNone(self.ss.single(user, card))


class ScheduleCreateTest(ScheduleTest):
    """
    Test all case invoke 'create' method
    """

    def test_create_with_empty_args(self):
        """
        Invoke 'create' with emtpy args
        :return: throw AssetsError exception
        """

        self.assertRaises(AssertionError, self.ss.create, None, None)

    def test_create(self):
        """
        Invoke 'create'
        :return: Schedule entity
        """

        user, card = self._create_test_user_and_card()
        schedule = self.ss.create(user, card)

        self.assertIsNotNone(schedule)

    def test_schedule_dates_is_valid(self):
        """
        Check all generated dates on valid.
        :return:
        """

        user, card = self._create_test_user_and_card()

        start = date(2016, 3, 4)

        schedule = self.ss.create(user, card, start)

        through_day = schedule.dates[0]['date'].date()
        through_three_days = schedule.dates[1]['date'].date()
        through_four_days = schedule.dates[2]['date'].date()
        through_thirty_days = schedule.dates[3]['date'].date()
        through_sixty_days = schedule.dates[4]['date'].date()

        self.assertEqual(through_day, date(2016, 3, 5))
        self.assertEqual(through_three_days, date(2016, 3, 7))
        self.assertEqual(through_four_days, date(2016, 3, 8))
        self.assertEqual(through_thirty_days, date(2016, 4, 3))
        self.assertEqual(through_sixty_days, date(2016, 5, 3))



