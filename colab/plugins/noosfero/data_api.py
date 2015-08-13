import json
import urllib
import urllib2
import logging

from dateutil.parser import parse

from django.conf import settings
from django.db.models.fields import DateTimeField

from colab.plugins.noosfero.models import (NoosferoArticle, NoosferoCommunity,
                                           NoosferoCategory)
from colab.plugins.utils.proxy_data_api import ProxyDataAPI

LOGGER = logging.getLogger('colab.plugin.debug')


class NoosferoDataAPI(ProxyDataAPI):

    def get_request_url(self, path, **kwargs):
        proxy_config = settings.COLAB_APPS.get(self.app_label, {})

        upstream = proxy_config.get('upstream')
        kwargs['private_token'] = proxy_config.get('private_token')
        params = urllib.urlencode(kwargs)

        if upstream[-1] == '/':
            upstream = upstream[:-1]

        return u'{}{}?{}'.format(upstream, path, params)

    def get_json_data(self, api_url, page, pages=1000):
        url = self.get_request_url(api_url, per_page=pages,
                                   page=page)
        try:
            data = urllib2.urlopen(url, timeout=10)
            json_data = json.load(data)
        except urllib2.URLError:
            LOGGER.exception("Connection timeout: " + url)
            json_data = []

        return json_data

    def fill_object_data(self, element, _object):
        for field in _object._meta.fields:
            try:
                if field.name == "user":
                    _object.update_user(
                        element["author"]["name"])
                    continue

                if field.name == "profile_identifier":
                    _object.profile_identifier = \
                        element["profile"]["identifier"]
                    continue

                if isinstance(field, DateTimeField):
                    value = parse(element[field.name])
                else:
                    value = element[field.name]

                setattr(_object, field.name, value)
            except KeyError:
                continue
            except TypeError:
                continue

        return _object

    def fetch_communities(self):
        json_data = self.get_json_data('/api/v1/communities', 1)

        json_data = json_data['communities']
        for element in json_data:
            community = NoosferoCommunity()
            self.fill_object_data(element, community)
            community.save()

            if 'categories' in element:
                for category_json in element["categories"]:
                    category = NoosferoCategory.objects.get_or_create(
                        id=category_json["id"], name=category_json["name"])[0]
                    community.categories.add(category.id)

    def fetch_articles(self):
        json_data = self.get_json_data('/api/v1/articles', 1)

        json_data = json_data['articles']

        for element in json_data:
            article = NoosferoArticle()
            self.fill_object_data(element, article)
            article.save()

            for category_json in element["categories"]:
                category = NoosferoCategory.objects.get_or_create(
                    id=category_json["id"], name=category_json["name"])[0]
                article.categories.add(category.id)

    def fetch_data(self):
        LOGGER.info("Importing Communities")
        self.fetch_communities()

        LOGGER.info("Importing Articles")
        self.fetch_articles()

    @property
    def app_label(self):
        return 'noosfero'
