# -*- coding: utf8 -*-

from django.template import RequestContext
from django.core.paginator import Paginator
from django.shortcuts import render_to_response, get_list_or_404

from super_archives import queries
from super_archives.models import MailingList


def thread(request, thread_token):

    first_message = queries.get_first_message_in_thread(thread_token)
    order_by = request.GET.get('order')
    if order_by == 'date':
        msgs_query = queries.get_messages_by_date()
    else:
        msgs_query = queries.get_messages_by_voted()
    
    msgs_query = msgs_query.filter(thread__subject_token=thread_token)
    emails = msgs_query.exclude(id=first_message.id)
    template_data = {
        'request': request,
        'first_msg': first_message,
        'emails': [first_message] + list(emails),
    }
    return render_to_response('message-thread.html', template_data, 
                              RequestContext(request))


def list_messages(request):
    
    order_by = request.GET.get('order')
    if order_by == 'voted':
        threads = queries.get_voted_threads()
    else:
        threads = queries.get_latest_threads()
    
    mail_list = request.GET.get('list')
    if mail_list:
        threads = threads.filter(mailinglist__name=mail_list)
    
    paginator = Paginator(threads, 16)
    page = int(request.GET.get('p', '1'))
    threads = paginator.page(page)
    
    lists = MailingList.objects.all()
    
    template_data = {
        'lists': lists,
        'n_results': paginator.count,
        'threads': threads,
        'request': request,
    }
    return render_to_response('message-list.html', template_data, 
                              RequestContext(request))