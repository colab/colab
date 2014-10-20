
from django_browserid.auth import BrowserIDBackend

class ColabBrowserIDBackend(BrowserIDBackend):
    def filter_users_by_email(self, email):
        return self.User.objects.filter(emails__address=email)
