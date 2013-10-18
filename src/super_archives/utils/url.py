# -*- coding: utf-8 -*-

def append_to_get(path, query=None, **kwargs):
# Getting the path with the query
    current_url = u'{}?{}'.format(
        path,
        query,
    )

    if kwargs and query:
        current_url += '&'

    for key, value in kwargs.items():
        # get the key, value to check if the pair exists in the query
        new = u'{}={}'.format(key, value)

        if new in current_url:
            continue

        if u'&{}='.format(key) not in current_url:
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
