from django.db import models
from django.conf import settings
from colab.accounts.models import User


class CollaborationModel(models.Model):
    '''
    Class to define the fields of the collaboration block
        that are displayed at dashboard and profile pages.
    '''

    @property
    def verbose_name(self):
        raise NotImplemented

    @property
    def tag(self):
        return None

    @property
    def title(self):
        raise NotImplemented

    @property
    def description(self):
        return None

    @property
    def url(self):
        return None

    @property
    def modified(self):
        return None

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

    @property
    def type(self):
        return None

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                             on_delete=models.SET_NULL)

    def update_user(self, user_name):
        self.user = User.objects.filter(username=user_name).last()

    class Meta:
        abstract = True
