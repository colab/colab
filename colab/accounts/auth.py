import re

from django_browserid.auth import BrowserIDBackend


class ColabBrowserIDBackend(BrowserIDBackend):
    def filter_users_by_email(self, email):
        return self.User.objects.filter(emails__address=email)

    def create_user(self, email):
        username = "colab_" + re.split('@', email)[0]
        password = None
        extra_fields = {
            'first_name': "Colab",
            'last_name': "Colab",
            }

        user = self.User.objects.filter(emails__address=email)

        if len(user) is not 0:
            return user

        return self.User.objects.create_user(
            username,
            email,
            password,
            **extra_fields
            )
