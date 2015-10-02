from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, Http404

from colab.plugins.utils.collaborations import get_collaboration_data
from colab.accounts.utils import mailman
from colab.accounts.models import User


def get_user_threads(threads, lists_for_user, key):
    visible_threads = []
    listnames_for_user = mailman.extract_listname_from_list(lists_for_user)
    for t in threads:
        if not t.mailinglist.is_private or \
           t.mailinglist.name in listnames_for_user:
            visible_threads.append(key(t))

    return visible_threads


def dashboard(request):
    """Dashboard page"""

    highest_score_threads = []  # TODO

    all_threads = []  # TODO
    latest_threads = []
    lists_for_user = []

    user = None
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user)
        lists_for_user = mailman.get_user_mailinglists(user)

    latest_threads = get_user_threads(
        all_threads, lists_for_user, lambda t: t)
    hottest_threads = get_user_threads(
        highest_score_threads, lists_for_user, lambda t: t.latest_message)

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
