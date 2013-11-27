import base64
import StringIO

from django import forms
from django.utils.translation import ugettext_lazy as _

from PIL import Image

from .models import Badge


class BadgeForm(forms.ModelForm):
    image = forms.ImageField(label=_(u'Image'))

    class Meta:
        model = Badge
        fields = (
            'title', 'description', 'image', 'user_attr', 'comparison',
            'value', 'awardees'
        )

    def save(self, commit=True):

        instance = super(BadgeForm, self).save(commit=False)

        img = Image.open(self.cleaned_data['image'])
        img = img.resize((50, 50), Image.ANTIALIAS)
        f = StringIO.StringIO()
        img.save(f, 'png')
        instance.image_base64 = f.getvalue().encode('base64')
        f.close()

        if commit:
            instance.save()

        return instance
