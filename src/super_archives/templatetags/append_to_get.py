# -*- coding: utf-8 -*-

import urllib
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def append_to_get(context, **kwargs):
    # Getting the path with the query
    current_url = u'{}?{}'.format(
        context['request'].META['PATH_INFO'],
        context['request'].META['QUERY_STRING'],
    )

    if kwargs and context['request'].META['QUERY_STRING']:
        current_url += '&'

    for key, value in kwargs.items():
        # get the key, value to check if the pair exists in the query
        new = u'{}={}'.format(key, value)

        if new in current_url:
            continue

        if key not in current_url:
            current_url += u'{}={}&'.format(key, value)
            continue

        parse_url = current_url.split(key)

        if len(parse_url) > 2:
            continue

        if unicode(value) in parse_url[1][1:]:
            continue

        check_kwargs_values = [
            False for value in kwargs.values()
            if unicode(value) not in parse_url[1]
        ]

        if not all(check_kwargs_values):
            list_remaining = parse_url[1][1:].split('&')
            real_remaining = u''

            if len(list_remaining) >= 2:
                real_remaining = u'&'.join(list_remaining[1:])

            current_url = u'{url}{key}={value}&{remaining}'.format(
                url=parse_url[0],
                key=key,
                value=value,
                remaining=real_remaining,
            )
            continue

        current_url = u'{url}{key}={value}+{remaining_get}'.format(
            url=parse_url[0],
            key=key,
            value=value,
            remaining_get=parse_url[1][1:],
        )
    if current_url[-1] == '&':
        return current_url[:-1]
    return current_url
