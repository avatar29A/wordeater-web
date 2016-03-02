# coding=utf-8
import config

from services.base import BaseService
from mongokit import ObjectId
from logger import logger, error

__author__ = 'Warlock'


class GroupService(BaseService):

    #
    # Public methods

    def list(self, user):
        """
        Returns all groups from database
        :return: list of Group
        """
        assert user is not None

        return list(self.db.Group.find({'user.$id': user.id}))

    def single(self, group_id=None, user=None, name=u""):
        """
        Returns group entity by:
        - ID
        - User and group's name
        - User. Returns a group where amount cards less than config.CARDS_IN_GROUP_AMOUNT

        Note: If you pass group_id with other arguments, the method will looking for by only group_id.

        :param group_id: Group ID
        :param user: Owner group
        :param name: Group's name
        :return: Group Enity
        """
        assert group_id or user, u"group_id or user_id always not None"

        if group_id:
            return self._get_by_group_id(group_id)

        if name:
            return self._get_by_user_and_name(user, name)

        return self._get_by_user(user)

    def create(self, user, name, descripton=u''):
        """
        Create a new group
        :param user: Owner
        :param name: Group name
        :param descripton: Group description
        :return: a group entity
        """

        assert user is not None and name, u"'user' and 'name' is required arguments"

        group = self.db.Group()
        group.user = user

        group.name = name
        group.description = descripton

        try:
            group.validate()
            group.save()
        except Exception as ex:
            logger.error(u"Group.create", ex.message)
            return None

        return group

    def rename(self, user, name, new_name):
        """
        Renames user's group. Method finds group by name and try rename it.
        :param user: Owner
        :param name: Current group name
        :param new_name: New group name
        :return: Group with new name or None
        """

        assert user is not None and name and new_name, u"'user', 'name' and 'new_name' is required parameters"

        group = self.single(user=user, name=name)
        if group is None:
            message = u'GroupServicce.rename. Group {0} not found'.format(name)
            logger.error(message)
            return None

        group.name = new_name

        try:
            group.validate()
            group.save()
        except Exception as ex:
            error(u"Group.rename", ex.message)
            return None

        return group

    def count(self, user):
        """
        Returns count of user's groups.
        :param user: Owner
        :return: list of group
        """
        assert user is not None

        return self.db.Group.find({'user.$id': user.id}).count()

    #
    # Private methods

    def _get_by_group_id(self, group_id):
        """
        Return group by id.
        :param group_id: str
        :return: group entity
        """

        group = self.db.Group.find_one({'_id': ObjectId(group_id)})
        return group

    def _get_by_user(self, user):
        """
        Returns user's group where words count less than 30.
        :param user:
        :param name:
        :return:
        """

        group = self.db.Group.find_one({'user.$id': user.id, 'cards_count':
            {'$lt': config.CARDS_IN_GROUP_AMOUNT}})

        if group is not None:
            return group

        group = self.create(user, self._generate_group_name(self.count(user)))
        return group

    def _get_by_user_and_name(self, user, name):
        """
        Search group by owner and group name
        :param self:
        :param user:
        :param name:
        :return:
        """

        group = self.db.Group.find_one({'user.$id': user.id, 'name': name})
        return group

    def _update_word_counter(self, group):
        """
        Update words counter
        :param group: Target group
        :return: Target group
        """
        group.cards_count = self.db.Card.find({'group.$id': group.id}).count()
        group.cards_studying_count = self.db.Card.find({'group.$id': group.id, 'is_studying': True}).count()

        try:
            group.validate()
            group.save()
        except Exception as ex:
            logger.error(u"Group.update_word_counter", ex.message)
        finally:
            return group

    @staticmethod
    def _generate_group_name(count):
        return u"Group #{0}".format(count + 1)