from django.conf.urls import patterns, include, url
from haystack.query import SearchQuerySet

from .forms import ColabSearchForm
from .views import ColabSearchView


urlpatterns = patterns('',
    url(r'^$', ColabSearchView(
        template='search/search.html',
        searchqueryset=SearchQuerySet(),
        form_class=ColabSearchForm,
    ), name='haystack_search'),
)
