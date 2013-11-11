# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Badge, BadgeI18N


class BadgeI18NInline(admin.TabularInline):
    model = BadgeI18N


class BadgeAdmin(admin.ModelAdmin):
    inlines = [BadgeI18NInline, ]


admin.site.register(Badge, BadgeAdmin)
