# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Badge


class BadgeForm(forms.ModelForm):
    description_en = forms.CharField(
        label=_(u'Description (English)'),
        required=False
    )
    description_es = forms.CharField(
        label=_(u'Description (Spanish)'),
        required=False
    )

    title_en = forms.CharField(label=_(u'Title (English)'), required=False)
    title_es = forms.CharField(label=_(u'Title (Spanish)'), required=False)

    class Meta:
        model = Badge
