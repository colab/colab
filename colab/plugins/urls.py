
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.core.exceptions import ImproperlyConfigured

undef_url_include_msg = (u'COLAB_APP with urls must define '
                          'the `include` attribute')
urlpatterns = patterns('')

for app_name, app in settings.COLAB_APPS.items():
    if not app or 'urls' not in app:
        continue

    urls = app.get('urls')
    if not urls.get('include'):
        raise ImproperlyConfigured(undef_url_include_msg)
    urlpatterns += patterns('',
        url(urls.get('prefix', r''), include(urls['include'],
            namespace=urls.get('namespace'))),
    )

