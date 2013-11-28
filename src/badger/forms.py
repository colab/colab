# -*- coding: utf-8 -*-

import base64

from django import forms
from django.utils.translation import ugettext_lazy as _

from PIL import Image

from .models import Badge

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class BadgeForm(forms.ModelForm):
    image = forms.ImageField(label=_(u'Image'), required=False)

    class Meta:
        model = Badge
        fields = (
            'title', 'description', 'image', 'user_attr', 'comparison',
            'value', 'awardees'
        )

    def clean_image(self):
        if not self.instance.pk and not self.cleaned_data['image']:
            raise forms.ValidationError(_(u'You must add an Image'))
        return self.cleaned_data['image']

    def save(self, commit=True):

        instance = super(BadgeForm, self).save(commit=False)

        if self.cleaned_data['image']:
            img = Image.open(self.cleaned_data['image'])
            img = img.resize((50, 50), Image.ANTIALIAS)
            f = StringIO()
            img.save(f, 'png')
            instance.image_base64 = f.getvalue().encode('base64')
            f.close()

        if commit:
            instance.save()

        return instance
