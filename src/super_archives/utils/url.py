# -*- coding: utf-8 -*-

import urllib
import urlparse


def append_to_get(path, query=None, **kwargs):
    query_dict = dict(urlparse.parse_qsl(query))
    for key, value in kwargs.items():
        query_dict[key] = value
    return u'{}?{}'.format(path, urllib.urlencode(query_dict))


def pop_from_get(path, query=None, **kwargs):
    # Getting the path with the query
    print query

    current_url = u'{}?{}'.format(
        path,
        query,
    )
    for key, value in kwargs.items():
        popitem = u'{}={}'.format(key, value)
        if query == popitem:
            return path

        if key not in current_url:
            return current_url

        first_path, end_path = current_url.split(key)
        end_path_without_element = end_path.split(value, 1)
        path_list = first_path + end_path_without_element
        print path_list
        return u''.join(path_list)
