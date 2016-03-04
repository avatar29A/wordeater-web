# coding=utf-8
import config
import datetime

from services.base import BaseService
from mongokit import ObjectId
from logger import logger, error

__author__ = 'Warlock'


class ScheduleService(BaseService):
    #
    # Public methods

    def create(self, user, card, start=None):
        """
        Create schedule for card.
        :param user: Card owner
        :param card: Card entity
        :param start: Day with which start calculate.
        :return: Schedule
        """

        assert user and card

        schedule = self.single(user, card)
        if schedule:
            return schedule

        schedule = self.db.Schedule()
        schedule.user = user
        schedule.card = card

        now = start if start is not None else datetime.date.today()

        # through one day:
        schedule.dates.append({
            'date': self._add_days(now, 1),
            'is_compleate': False
        })

        # through three_day
        schedule.dates.append({
            'date': self._add_days(now, 3),
            'is_compleate': False
        })

        schedule.dates.append({
            'date': self._add_days(now, 4),
            'is_compleate': False
        })

        schedule.dates.append({
            'date': self._add_days(now, 30),
            'is_compleate': False
        })

        schedule.dates.append({
            'date': self._add_days(now, 60),
            'is_compleate': False
        })

        try:
            schedule.validate()
            schedule.save()
        except Exception as ex:
            logger.error(ex.message)
            return None

        return schedule

    def single(self, user, card):
        """
        Search schedule for Card (by user.id and card.id)
        :param user: Card owner
        :param card: Card entity
        :return: Schedule for card
        """
        assert user and card, u"User and Card can't be is None"

        return self.db.Schedule.find_one({'user.$id': user.id, 'card.$id': card.id})

    #
    # Private methods:

    @staticmethod
    def _add_days(date, days):
        """
        Add few days to date
        :param date: current date
        :param days: amount days which need to add.
        :return: new date
        """

        return datetime.datetime.combine(date + datetime.timedelta(days=days), datetime.datetime.min.time())

