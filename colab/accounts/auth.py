from django_browserid.auth import BrowserIDBackend, default_username_algo


class ColabBrowserIDBackend(BrowserIDBackend):
    def filter_users_by_email(self, email):
        return self.User.objects.filter(emails__address=email)

    def create_user(self, email):
        username = default_username_algo(email)
        password = None
        extra_fields = {
            'needs_update': True
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
