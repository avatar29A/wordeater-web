# coding=utf-8

from model import *
from users import User

__author__ = 'Glebov Boris'


@db.register
class Group(BaseDocument):
    """
    Description group entity
    """
    __collection__ = "groups"

    structure = {
        'user': User,
        'name': unicode,
        'description': unicode,
        'cards_count': int,
        'cards_studying_count': int,
        'create_date': datetime.datetime
    }

    default_values = {
        'create_date': datetime.datetime.now(),
        'cards_count': 0,
        'cards_studying_count': 0
    }

    @property
    def cards(self):
        return db.Card.find({"group.$id": self.id})

    @staticmethod
    def list(user):
        """
        Returns all groups from database
        :return: list of Group
        """

        return list(db.Group.find({'user.$id': user.id}))

    @staticmethod
    def single(group_id=None, user=None, name=u""):
        assert group_id is not None or user is not None, u"group_id or user_id always not None"
        assert len(name) > 0 and user is not None

        if group_id is not None:
            return Group._get_by_group_id(group_id)

        if len(name) > 0:
            return Group._get_by_user_and_name(user, name)

        return Group._get_by_user(user)

    @staticmethod
    def _get_by_group_id(group_id):
        """
        Return group by id.
        :param group_id: str
        :return: group entity
        """

        group = db.Group.find_one({'_id': ObjectId(group_id)})
        return group

    @staticmethod
    def _get_by_user(user):
        """
        Returns user's group where words count less than 30.
        :param user:
        :param name:
        :return:
        """

        group = db.Group.find_one({'user.$id': user.id, 'cards_count':
            {'$lt': config.CARDS_IN_GROUP_AMOUNT}})

        if group is not None:
            return group

        group = Group.create(user, Group._generate_group_name(Group.count(user)))
        return group

    @staticmethod
    def _get_by_user_and_name(user, name):
        """
        Search group by owner and group name
        :param self:
        :param user:
        :param name:
        :return:
        """

        group = db.Group.find_one({'user.$id': user.id, 'name': name})
        return group

    @staticmethod
    def _update_word_counter(group):
        """
        Update words counter
        :param group: Target group
        :return: Target group
        """
        group.cards_count = db.Card.find({'group.$id': group.id}).count()
        group.cards_studying_count = db.Card.find({'group.$id': group.id, 'is_studying': True}).count()

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

    @staticmethod
    def create(user, name, descripton=u''):
        """
        Create a new group
        :param user: Owner
        :param name: Group name
        :param descripton: Group description
        :return: a group entity
        """

        group = db.Group()
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

    @staticmethod
    def rename(user, name, new_name):
        """
        Renames user's group
        :param user: Owner
        :param name: Current group name
        :return:
        """

        group = Group.single(user=user, name=name)
        if group is None:
            message = u'Expected group {0} not found'.format(name)
            logger.error(u"Group.rename", message)

            raise Exception(message)

        group.name = new_name

        try:
            group.validate()
            group.save()
        except Exception as ex:
            logger.error(u"Group.rename", ex.message)
            return None

        return group
