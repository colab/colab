from django.shortcuts import render

from django.utils import timezone

from haystack.query import SearchQuerySet
from super_archives import queries


def index(request):
    """Index page view"""

    latest_threads = queries.get_latest_threads()
    hottest_threads = queries.get_hottest_threads()

    count_types = {}
    six_months = timezone.now() - timezone.timedelta(days=180)
    for type in ['wiki', 'thread', 'changeset', 'ticket']:
        count_types[type] = SearchQuerySet().filter(
            type=type,
            modified__gte=six_months,
        ).count()

    context = {
        'hottest_threads': hottest_threads[:6],
        'latest_threads': latest_threads[:6],
        'type_count': count_types,
        'latest_results': SearchQuerySet().all().order_by(
            '-modified', '-created'
        )[:6],
    }
    return render(request, 'home.html', context)
