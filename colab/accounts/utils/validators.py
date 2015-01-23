
import urllib2
import urlparse


def validate_social_account(account, url):
    """Verifies if a social account is valid.

    Examples:

    >>> validate_social_account('seocam', 'http://twitter.com')
    True

    >>> validate_social_account('seocam-fake-should-fail',
                                'http://twitter.com')
    False

    """

    request = urllib2.Request(urlparse.urljoin(url, account))
    request.get_method = lambda: 'HEAD'

    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError:
        return False

    return response.code == 200
