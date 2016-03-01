# coding=utf-8
__author__ = 'Warlock'

import config

from services.base import BaseService
from logger import logger
from mongokit import ObjectId


class GroupService(BaseService):

    def list(self, user):
        """
        Returns all groups from database
        :return: list of Group
        """

        return list(self.connection.Group.find({'user.$id': user.id}))

    def create(self, user, name, descripton=u''):
        """
        Create a new group
        :param user: Owner
        :param name: Group name
        :param descripton: Group description
        :return: a group entity
        """

        group = self.connection.Group()
        group.user = user

        group.name = name
        group.description = descripton

        try:
            group.validate()
            group.save()
        except Exception as ex:
            logger.error(ex.message)
            return None

        return group

    def rename(self, user, name, new_name):
        """
        Renames user's group
        :param user: Owner
        :param name: Current group name
        :return:
        """

        group = self.get(user, name)
        if group is None:
            message = u'Expected group {0} not found'.format(name)
            logger.error(message)

            raise Exception(message)

        group.name = new_name

        try:
            group.validate()
            group.save()
        except Exception as ex:
            logger.error(ex.message)
            return None

        return group

    def clear(self):
        """
        Remove all records in collections
        :return: count removed records
        """

        count = self.connection.Group.find().count()

        try:
            self.connection.Group.drop()
        except Exception as ex:
            logger.error(ex.message)

            return 0

        return count

    def count(self, user):
        """
        Return amount elements in collections
        :param user: Owner
        :return: amount elements in collections
        """
        return self.connection.Group.find({'user.$id': user.id}).count()

    def get(self, user):
        """
        Returns user's group where words count less than 30.
        :param user:
        :param name:
        :return:
        """

        group = self.connection.Group.find_one({'user.$id': user.id, 'cards_count':
            {'$lt': config.CARDS_IN_GROUP_AMOUNT}})

        if group is not None:
            return group

        group = self.create(user, self._generate_group_name(self.count(user)))
        return group

    def get_one(self, group_id):
        """
        Return group by id.
        :param group_id: str
        :return: group entity
        """

        group = self.connection.Group.find_one({'_id': ObjectId(group_id)})
        return group


    def update_word_counter(self, group):
        """
        Update words counter
        :param group: Target group
        :return: Target group
        """
        group.cards_count = self.connection.Card.find({'group.$id': group.id}).count()
        group.cards_studying_count = self.connection.Card.find({'group.$id': group.id, 'is_studying': True}).count()

        try:
            group.validate()
            group.save()
        except Exception as ex:
            logger.error(ex.message)
        finally:
            return group

    @staticmethod
    def _generate_group_name(count):
        return u"Group #{0}".format(count + 1)