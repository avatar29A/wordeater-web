# -*- coding: utf-8 -*-
import json
from mongokit import ObjectId

__author__ = 'Glebov Boris'


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

#using:
#JSONEncoder().encode(analytics)