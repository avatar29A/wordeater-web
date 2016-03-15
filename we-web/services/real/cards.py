# coding=utf-8

from services.base import BaseService
from logger import logger

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
        card.group = group

        try:
            card.validate()
            card.save()

            # Update amount cards in group
            group.cards_count += 1
            group.save()
        except Exception as ex:
            logger.error(u'Card.create', ex)
            return None

        return card

    def single(self, user, text, lang):
        """
        Return card by user's login and native word
        :param user: User entity
        :param text: native word
        :param lang: language
        :return:
        """

        card = self.db.Card.find_one({'user.$id': user.id,
                                      'text': {'$elemMatch': {'lang': lang, 'value': text}}})

        return card

    def to_native(self, card):
        """
        Returns a native card text
        :param card: Card
        :return: native text
        """

        assert card and card.user

        return card.native

    def to_foreign(self, card):
        """
        Returns a foreign card text
        :param card: Card
        :return: foreign text
        """

        assert card and card.user

        return card.foreign
