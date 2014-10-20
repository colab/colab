
from django.conf import settings

from hitcounter.views import HitCounterViewMixin

from ..utils.views import ColabProxyView
from .models import Wiki, Ticket, Revision


class TracProxyView(HitCounterViewMixin, ColabProxyView):
    app_label = 'trac'
    diazo_theme_template = 'proxy/trac.html'

    def get_object(self):
        obj = None

        if self.request.path_info.startswith('/wiki'):
            wiki_name = self.request.path_info.split('/', 2)[-1]
            if not wiki_name:
                wiki_name = 'WikiStart'
            try:
                obj = Wiki.objects.get(name=wiki_name)
            except Wiki.DoesNotExist:
                return None
        elif self.request.path_info.startswith('/ticket'):
            ticket_id = self.request.path_info.split('/')[2]
            try:
                obj = Ticket.objects.get(id=ticket_id)
            except (Ticket.DoesNotExist, ValueError):
                return None
        elif self.request.path_info.startswith('/changeset'):
            try:
                changeset, repo = self.request.path_info.split('/')[2:4]
            except ValueError:
                return None
            try:
                obj = Revision.objects.get(rev=changeset,
                                           repository_name=repo)
            except Revision.DoesNotExist:
                return None

        return obj
