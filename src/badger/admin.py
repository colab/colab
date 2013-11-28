# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .forms import BadgeForm
from .models import Badge, BadgeI18N


class BadgeI18NInline(admin.TabularInline):
    model = BadgeI18N


class BadgeAdmin(admin.ModelAdmin):
    form = BadgeForm
    inlines = [BadgeI18NInline, ]
    list_display = ['title', 'description', 'order']
    list_editable = ['order', ]


admin.site.register(Badge, BadgeAdmin)
