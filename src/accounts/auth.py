
from django_browserid.auth import BrowserIDBackend

class ColabBrowserIDBackend(BrowserIDBackend):
    def filter_users_by_email(self, email):
        return self.User.objects.filter(emails__address=email)

    def authenticate(self, *args, **kw):
        #import pdb; pdb.set_trace();
        return super(ColabBrowserIDBackend, self).authenticate(*args, **kw)
