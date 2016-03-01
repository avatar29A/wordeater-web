# coding=utf-8
__author__ = 'Warlock'


def group_to_dict(group):
    return {'id': str(group.id),
            'name': group.name,
            'description': group.description,
            'cards_count': group.cards_count,
            'cards_studying_count': group.cards_studying_count,
            'create_date': group.create_date.strftime("%d %B %Y")}