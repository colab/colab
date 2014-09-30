#!/usr/bin/env python

from django.core.management.base import BaseCommand
from colab.super_archives.models import Message


class Command(BaseCommand):
    help = "Update message blocks (used to hide the reply part messages)"

    def handle(self, *args, **kwargs):
        for message in Message.objects.iterator():
            message.update_blocks()
