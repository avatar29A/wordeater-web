# coding=utf-8

from model import *
from users import User
from groups import Group


@db.register
class Card(BaseDocument):
    """
    Card entity
    """
    __collection__ = "cards"

    structure = {
        # Ref
        'user': User,
        'group': Group,
        # Fields
        'text': unicode,
        'transcription': unicode,
        'context': unicode,
        'image_url': unicode,
        'is_studying': bool,
        'is_done': bool,
        'create_date': datetime.datetime
    }

    i18n = ['text', 'context', 'transcription']
    default_values = {
        'create_date': datetime.datetime.now(),
        'is_studying': True,
        'is_done': False
    }

    @staticmethod
    def list(user):
        """
        Returns user's cards
        :param user: User entity
        :return: list of user's card
        """

        return list(db.Card.find({'user.$id': user.id}))

    @staticmethod
    def single(user_id, text, lang):
        """
        Return card by user's login and native word
        :param user_id:
        :param text: native word
        :param lang: language
        :return:
        """

        card = db.Card.find_one({'user.$id': user_id,
                                              'text': {'$elemMatch': {'lang': lang, 'value': text}}})

        return card

    @staticmethod
    def create(user,
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

        card = db.Card(lang=user.native_lng, fallback_lang=user.native_lng)

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
        except Exception as ex:
            logger.error(u'Card.create', ex)
            return None

        return card