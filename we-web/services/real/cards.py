# coding=utf-8
__author__ = 'Warlock'

from services.base import BaseService
from services.groups import GroupService

from logger import logger


class CardService(BaseService):
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