# coding=utf-8
__author__ = 'Warlock'


def card_to_dict_for_learn(card):
    """
    DTO word for learn
    :param card:
    :return:
    """

    card.set_lang(card.user.native_lng)
    native = card.text

    card.set_lang(card.user.foreign_lng)
    foreigne = card.text
    context = card.context,
    transcription = card.transcription

    return {
        'id': str(card.id),
        'native': native,
        'foreigne': foreigne,
        'context': context,
        'transcription': transcription
    }