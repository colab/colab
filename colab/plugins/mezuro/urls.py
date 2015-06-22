from django.conf.urls import patterns, url
from .views import MezuroProxyView

urlpatterns = patterns('',
    # Gitlab URLs
    url(r'^(?P<path>.*)$', MezuroProxyView.as_view(), name='mezuro'),
)
