# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from haystack.query import SearchQuerySet

from accounts.models import User
from badger.models import Badge


class Command(BaseCommand):
    help = "Rebuild the user's badges."

    def handle(self, *args, **kwargs):
        for badge in Badge.objects.filter(type='auto'):
            if not badge.comparison:
                continue
            elif badge.comparison == 'biggest':
                order = u'-{}'.format(Badge.USER_ATTR_OPTS[badge.user_attr])
                sqs = SearchQuerySet().filter(type='user')
                user = sqs.order_by(order)[0]
                badge.awardees.remove(*list(badge.awardees.all()))
                badge.awardees.add(User.objects.get(pk=user.pk))
                continue

            comparison = u'__{}'.format(badge.comparison) if badge.comparison \
                    is not 'equal' else u''

            key = u'{}{}'.format(
                Badge.USER_ATTR_OPTS[badge.user_attr],
                comparison
            )
            opts = {key: badge.value}

            sqs = SearchQuerySet().filter(
                type='user',
                **opts
            )

            # Remove all awardees to make sure that all of then
            # still accomplish the necessary to keep the badge
            badge.awardees.remove(*list(badge.awardees.all()))

            for user in sqs:
                badge.awardees.add(User.objects.get(pk=user.pk))
