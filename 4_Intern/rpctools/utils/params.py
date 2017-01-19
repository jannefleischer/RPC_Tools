# -*- coding: utf-8 -*-

from collections import OrderedDict


class Params(object):
    """Parameter class like an ordered dict"""
    def __init__(self, *args, **kwargs):
        self._od = OrderedDict(*args, **kwargs)
    def __getattr__(self, name):
        return self._od[name]
    def __setattr__(self, name, value):
        if name == '_od':
            self.__dict__['_od'] = value
        else:
            self._od[name] = value
    def __delattr__(self, name):
        del self._od[name]

    def __getitem__(self, i):
        return self._od.values()[i]

    def __setitem__(self, i, value):
        self._od.items()[i] = value