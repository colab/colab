# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .forms import BadgeForm
from .models import Badge


class BadgeAdmin(admin.ModelAdmin):
    form = BadgeForm
    fieldsets = (
        (None, {
            'fields': (
                'title', 'description', 'image', 'type', 'user_attr',
                'comparison', 'value',
            )
        }),
        (_(u'Translatable items - English'), {
            'classes': ('collapse', ),
            'fields': ('title_en', 'description_en'),
        }),
        (_(u'Translatable items - Spanish'), {
            'classes': ('collapse', ),
            'fields': ('title_es', 'description_es'),
        })
    )


admin.site.register(Badge, BadgeAdmin)
