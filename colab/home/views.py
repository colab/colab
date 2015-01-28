from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, Http404

from colab.search.utils import get_collaboration_data
from colab.super_archives.models import Thread


def dashboard(request):
    """Dashboard page"""

    highest_score_threads = Thread.highest_score.all()[:6]

    hottest_threads = [t.latest_message for t in highest_score_threads]

    latest_threads = Thread.objects.all()[:6]

    latest_results, count_types = get_collaboration_data()
    latest_results.sort(key=lambda elem: elem.modified, reverse=True)

    context = {
        'hottest_threads': hottest_threads[:6],
        'latest_threads': latest_threads,
        'type_count': count_types,
        'latest_results': latest_results[:6],
    }
    return render(request, 'home.html', context)


def robots(request):
    if getattr(settings, 'ROBOTS_NOINDEX', False):
        return HttpResponse('User-agent: *\nDisallow: /',
                            content_type='text/plain')

    raise Http404
