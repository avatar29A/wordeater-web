# coding=utf-8
import json

from services.base import BaseService
from services.service_locator import ServiceLocator
from logger import error

__author__ = 'Warlock'


class CardService(BaseService):

    #
    # Public interface

    def list(self, user):
        """
        Returns user's cards
        :param user: User entity
        :return: list of user's card
        """

        assert user, u"User could't be None"

        return list(self.db.Card.find({'user.$id': user.id}))

    def create(self,
               user,
               group,
               foreign,
               native,
               transcription=u'',
               context=u'',
               image_url=u''):
        """
        Create new card
        :param group: it's group where a card need to add. .
        :param image_url:
        :param context:
        :param transcription:
        :param user: Owner
        :param native: Native word
        :param foreign: Translated word
        :return: a new card
        """

        assert user and group, u'User and Group is not none parameters'
        assert foreign and native, u'Foreign and Native is not empty parameters'

        card = self.db.Card(lang=user.native_lng, fallback_lang=user.native_lng)

        card.user = user

        # set native field
        card.native = native
        card.foreign = foreign
        card.transcription = transcription
        card.image_url = image_url

        # Try to set context:
        card.foreign_context = context if context else self._get_context(card.foreign)

        # Link with group:
        card.group = group

        try:
            card.validate()
            card.save()

            # Update amount cards in group
            group.cards_count += 1
            group.save()
        except Exception as ex:
            error(u'Card.create', ex)
            return None

        return card

    def get(self, user, card_id):
        """
        Returns card by user's id and card's id
        :param user: User ID -> User
        :param card_id: Card ID -> ObjectId
        :return: Card entity
        """

        card = self.db.Card.find_one({'_id': card_id, 'user.$id': user.id})

        return card

    def single(self, user, text, lang):
        """
        Returns card by user's id and native word
        :param user: User entity
        :param text: native word
        :param lang: language
        :return:
        """

        card = self.db.Card.find_one({'user.$id': user.id,
                                      'text': {'$elemMatch': {'lang': lang, 'value': text}}})

        return card

    def exists(self, user, text, lang):
        """
         Returns True if card is exists
        :param user: User entity
        :param text: native word
        :param lang: language
        """

        return self.single(user, text, lang) is not None

    @staticmethod
    def _get_context(text):
        vs = ServiceLocator.resolve(ServiceLocator.VOCABULARITY)

        return vs.get_context(text)
