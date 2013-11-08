# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from accounts.models import User
from badger.utils import get_counters_to_badge
from badger.models import Badge


class Command(BaseCommand):
    help = "Update the user's badges"

    def handle(self, *args, **kwargs):
        for badge in Badge.objects.filter(type='auto'):
            if not badge.comparison:
                continue
            for user in User.objects.all():
                user_counters = get_counters_to_badge(user)

                # TODO remove user if it doesn't sastify the conditions of the
                # badge anymore
                if badge.comparison == 'gte':
                    if user_counters[badge.user_attr] >= badge.value:
                        badge.awardees.add(user)
                elif badge.comparison == 'lte':
                    if user_counters[badge.user_attr] <= badge.value:
                        badge.awardees.add(user)
                elif badge.comparison == 'equal':
                    if user_counters[badge.user_attr] == badge.value:
                        badge.awardees.add(user)
