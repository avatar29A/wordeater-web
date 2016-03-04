# -*- coding: utf-8 -*-
import time
from datetime import datetime
from mongokit import ObjectId

__author__ = 'Glebov Boris'


def fill(source, dist, exclude):
    for item in source.iteritems():
        key = item[0]
        value = item[1]

        if key in exclude or key != '$id' and key[0] == '$':
            continue

        if key == '$id':
            if not value:
                continue

            dist['_id'] = ObjectId(value['$oid'])
        elif isinstance(dist[key], dict):
            fill(value, dist[key], [])
        else:
            dist_key_type = type(dist[key])

            if dist_key_type is type(None):
                dist[key] = value
            else:
                dist[key] = mapping_convert_function[dist_key_type](value)

    return dist


def to_objectid(objectId):
    if isinstance(objectId, str) or isinstance(objectId, unicode):
        return ObjectId(objectId)
    elif isinstance(objectId, dict) and '$oid' in objectId:
        return ObjectId(objectId['$oid'])
    else:
        raise Exception(u"{0} not supported".format(objectId))


def _convert_to_int(value):
    return int(value)


def _convert_to_float(value):
    if type(value) is str:
        return float(value.replace(',', '.'))
    else:
        return float(value)


def _convert_to_objectid(value):
    return ObjectId(value)


def _convert_to_datetime(value):
    if not type(value) is str:
        return value

    format_str = time.strptime(value, "%d.%m.%y")
    return datetime.fromtimestamp(time.mktime(format_str))


def _convert_to_bool(value):
    return bool(value)


def _convert_to_str(value):
    return str(value)


def _convert_to_unicode(value):
    return unicode(value)


mapping_convert_function = {
    int: _convert_to_int,
    float: _convert_to_float,
    bool: _convert_to_bool,
    ObjectId: _convert_to_objectid,
    datetime: _convert_to_datetime,
    unicode: _convert_to_unicode,
    str: _convert_to_str
}
