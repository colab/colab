# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from haystack.query import SearchQuerySet

from accounts.models import User
from badger.models import Badge

import logging

class Command(BaseCommand):
    help = "Update the user's badges"

    def search(self, object_type, **opts={}):
        try:
            sqs = SearchQuerySet().filter(type=object_type, **opts)
        except Exception, e:
            logging.except(e)
            raise
        return sqs

    def handle(self, *args, **kwargs):
        for badge in Badge.objects.filter(type='auto'):
            if not badge.comparison:
                continue
            elif badge.comparison == 'biggest':
                order = u'-{}'.format(Badge.USER_ATTR_OPTS[badge.user_attr])
                sqs = self.search('user')
                user = sqs.order_by(order)[0]
                badge.awardees.add(User.objects.get(pk=user.pk))
                continue

            comparison = u'__{}'.format(badge.comparison) if badge.comparison \
                    is not 'equal' else u''

            key = u'{}{}'.format(
                Badge.USER_ATTR_OPTS[badge.user_attr],
                comparison
            )
            opts = {key: badge.value}

            sqs = self.search('user', **opts)

            for user in sqs:
                badge.awardees.add(User.objects.get(pk=user.pk))
