
from collections import OrderedDict

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponse, Http404

from search.utils import trans
from haystack.query import SearchQuerySet

from proxy.models import WikiCollabCount, TicketCollabCount
from super_archives.models import Thread


def index(request):
    """Index page view"""


    latest_threads = Thread.objects.all()[:6]
    hottest_threads = Thread.highest_score.from_haystack()[:6]

    count_types = cache.get('home_chart')
    if count_types is None:
        count_types = OrderedDict()
        for type in ['thread', 'changeset', 'attachment']:
            count_types[trans(type)] = SearchQuerySet().filter(
                type=type,
            ).count()

        count_types[trans('ticket')] = sum([
            ticket.count for ticket in TicketCollabCount.objects.all()
        ])

        count_types[trans('wiki')] = sum([
            wiki.count for wiki in WikiCollabCount.objects.all()
        ])
        cache.set('home_chart', count_types)

    context = {
        'hottest_threads': hottest_threads[:6],
        'latest_threads': latest_threads,
        'type_count': count_types,
        'latest_results': SearchQuerySet().all().order_by(
            '-modified', '-created'
        )[:6],
    }
    return render(request, 'home.html', context)


def robots(request):
    if settings.ROBOTS_NOINDEX:
        return HttpResponse('User-agent: *\nDisallow: /',
                            content_type='text/plain')

    raise Http404
