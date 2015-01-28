from django.db import models
from django.conf import settings
from colab.accounts.models import User


class Collaboration(models.Model):
    '''
    Class to define the fields of the collaboration block
        that are displayed at dashboard and profile pages.
    '''

    tag = None
    title = None
    description = None
    url = None
    modified = None
    type = None

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                             on_delete=models.SET_NULL)

    @property
    def modified_by(self):
        if self.user:
            return self.user.get_full_name()
        return None

    @property
    def modified_by_url(self):
        if self.user:
            return self.user.get_absolute_url()
        return None

    def update_user(self, user_name):
        try:
            self.user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            self.user = None

    class Meta:
        abstract = True
