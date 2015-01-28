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
        if query_dict not in (key):
            continue
        if query_dict[key] == value:
            del query_dict[key]
            continue
        if value in query_dict[key]:
            aux = query_dict[key].split(value)
            query_dict[key] = u''.join(aux).strip()
    return u'{}?{}'.format(path, urllib.urlencode(query_dict))
