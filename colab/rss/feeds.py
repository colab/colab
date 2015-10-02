#!/usr/bin/env python
# encoding: utf-8

from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext as _

from haystack.query import SearchQuerySet

class LatestThreadsFeeds(Feed):
    title = _(u'Latest Discussions')
    link = '/rss/threads/latest/'

    def items(self):
        return []

    def item_link(self, item):
        return item.latest_message.url

    def item_title(self, item):
        title = '[' + item.mailinglist.name + '] '
        title += item.latest_message.subject_clean
        return title

    def item_description(self, item):
        return item.latest_message.body


class HottestThreadsFeeds(Feed):
    title = _(u'Discussions Most Relevance')
    link = '/rss/threads/hottest/'

    def items(self):
        return []

    def item_link(self, item):
        return item.latest_message.url

    def item_title(self, item):
        title = '[' + item.mailinglist.name + '] '
        title += item.latest_message.subject_clean
        return title

    def item_description(self, item):
        return item.latest_message.body


class LatestColabFeeds(Feed):
    title = _(u'Latest collaborations')
    link = '/rss/colab/latest/'

    def items(self):
        items = SearchQuerySet().order_by('-modified', '-created')[:20]
        return items

    def item_title(self, item):
        type_ = item.type + ': '
        mailinglist = item.tag

        if mailinglist:
            prefix = type_ + mailinglist + ' - '
        else:
            prefix = type_

        return prefix + item.title

    def item_description(self, item):
        return item.latest_description

    def item_link(self, item):
        return item.url
