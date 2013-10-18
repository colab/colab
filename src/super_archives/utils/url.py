# -*- coding: utf-8 -*-

import urllib
import urlparse


def append_to_get(path, query=None, **kwargs):
    query_dict = dict(urlparse.parse_qsl(query))
    for key, value in kwargs.items():
        query_dict[key] = value
    return u'{}?{}'.format(path, urllib.urlencode(query_dict))


def pop_from_get(path, query=None, **kwargs):
    query_dict = dict(urlparse.parse_qsl(query))
    for key, value in kwargs.items():
        if not query_dict.has_key(key):
            continue
        if query_dict[key] == value:
            del query_dict[key]
            continue
    if not query_dict:
        return u'{}?q='.format(path)
    return u'{}?{}'.format(path, urllib.urlencode(query_dict))
