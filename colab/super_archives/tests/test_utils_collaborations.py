# -*- coding:utf-8 -*-

from django.test import TestCase
from colab.super_archives.utils.collaborations import count_threads


class CollaborationTest(TestCase):

    fixtures = ['mailinglistdata.json']

    def test_count_threads(self):
        self.assertEquals(count_threads(), 5)
