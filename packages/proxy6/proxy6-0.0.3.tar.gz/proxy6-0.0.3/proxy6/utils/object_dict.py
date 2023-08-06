#!/usr/bin/env python
# coding: utf8

from __future__ import unicode_literals

import json
from copy import deepcopy


class ObjectDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

    def __str__(self):
        obj = deepcopy(self)
        if '_id' in obj:
            obj._id = 'ObjectId(\'{}\')'.format(str(self._id))
        return json.dumps(obj, ensure_ascii=False, indent=4, sort_keys=True).encode('utf-8')
