# coding=utf-8
__author__ = 'Warlock'

from services.base import BaseService
from services.groups import GroupService

from logger import logger


class CardService(BaseService):
    def list(self, user):
        """
        Returns user's cards
        :return: list of user's card
        """

        return list(self.connection.Card.find({'user.$id': user.id}))

    def create(self,
               user,
               foreign,
               native,
               transcription=u'', context=u'', image_url=u''):
        """
        Create new card
        :param user: Owner
        :param native: Native word
        :param foreign: Translated word
        :return: a new card
        """

        card = self.get(user.id, native, user.native_lng)
        if card is not None:
            return card

        card = self.connection.Card(lang=user.native_lng, fallback_lang=user.native_lng)

        card.user = user

        # set native field
        card.text = native

        # set foreign field
        card.set_lang(user.foreign_lng)

        card.text = foreign
        card.context = context
        card.transcription = transcription

        # Optional:
        card.transcription = transcription
        card.image_url = image_url

        # Link with group:
        group_service = GroupService(db)
        card.group = group_service.get(user)

        try:
            card.validate()
            card.save()

            group_service.update_word_counter(card.group)
        except Exception as ex:
            logger.error(ex.message)
            return None

        return card

    def clear(self):
        """
        Remove all cards from database
        :return: count of removed cards.
        """

        count = self.connection.Card.find().count()
        self.connection.Card.drop()

        return count

    def get(self, user_id, text, lang):
        """
        Return card by user's login and native word
        :param user:
        :param native: native word
        :return:
        """

        card = self.connection.Card.find_one({'user.$id': user_id,
                                              'text': {'$elemMatch': {'lang': lang, 'value': text}}})

        return card

if __name__ == '__main__':
    from domain.model import db
    from services.users import UserService

    us = UserService(db)
    cs = CardService(db)

    user = us.get(u'warlock')

    for i in range(0, 30):
        card = cs.create(user, u'dog{0}'.format(i), u'cane{0}'.format(i))
        print card