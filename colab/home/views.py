from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, Http404

from colab.search.utils import trans, getCollaborationData
from colab.super_archives.models import Thread


def dashboard(request):
    """Dashboard page"""

    latest_threads = Thread.objects.all()[:6]
    highest_score_threads = Thread.highest_score.all()[:6]

    hottest_threads = []
    for thread in highest_score_threads:
        hottest_threads.append(thread.latest_message)

    latest_results, count_types = getCollaborationData()
    threads = Thread.objects.all()
    messages = []
    for t in threads:
        messages.append(t.latest_message)

    latest_results.extend(messages)
    latest_results = sorted(latest_results,
                            key=lambda elem: elem.modified, reverse=True)

    for key in count_types.keys():
        count_types[trans(key)] = count_types.pop(key)

    context = {
        'hottest_threads': hottest_threads[:6],
        'latest_threads': latest_threads[:6],
        'type_count': count_types,
        'latest_results': latest_results[:6],
    }
    return render(request, 'home.html', context)


def robots(request):
    if getattr(settings, 'ROBOTS_NOINDEX', False):
        return HttpResponse('User-agent: *\nDisallow: /',
                            content_type='text/plain')

    raise Http404
