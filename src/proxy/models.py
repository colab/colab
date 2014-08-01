# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

if settings.TRAC_ENABLED:
    import trac.trac.models
