
from collections import OrderedDict

from django.shortcuts import render

from search.utils import trans
from haystack.query import SearchQuerySet

from super_archives.models import Thread


def index(request):
    """Index page view"""


    latest_threads = Thread.objects.all()[:6]
    hottest_threads = Thread.highest_score.from_haystack()[:6]

    count_types = OrderedDict()
    for type in ['thread', 'ticket', 'wiki', 'changeset', 'attachment']:
        count_types[trans(type)] = SearchQuerySet().filter(
            type=type,
        ).count()

    context = {
        'hottest_threads': hottest_threads[:6],
        'latest_threads': latest_threads,
        'type_count': count_types,
        'latest_results': SearchQuerySet().all().order_by(
            '-modified', '-created'
        )[:6],
    }
    return render(request, 'home.html', context)
