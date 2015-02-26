from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, Http404

from colab.search.utils import get_collaboration_data
from colab.super_archives.models import Thread
from colab.accounts.utils import mailman
from colab.accounts.models import User


def dashboard(request):
    """Dashboard page"""

    highest_score_threads = Thread.highest_score.all()

    all_threads = Thread.objects.all()
    latest_threads = []
    lists_for_user = []

    user = None
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user)
        lists_for_user = mailman.get_user_mailinglists(user)

    for t in all_threads:
        if not t.mailinglist.is_private or \
           t.mailinglist.name in lists_for_user:
                latest_threads.append(t)

    hottest_threads = []
    for t in highest_score_threads:
        if not t.mailinglist.is_private or \
           t.mailinglist.name in lists_for_user:
                hottest_threads.append(t.latest_message)

    latest_results, count_types = get_collaboration_data(user)
    latest_results.sort(key=lambda elem: elem.modified, reverse=True)

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
