from django.contrib import admin

from .models import Badge


class BadgeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Badge, BadgeAdmin)
