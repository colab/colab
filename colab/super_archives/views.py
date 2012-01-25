# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.core.paginator import Paginator
from django.shortcuts import render_to_response, get_list_or_404

from colab.super_archives import queries
from colab.super_archives.models import MailingList, Thread


def thread(request, thread_token):

    first_message = queries.get_first_message_in_thread(thread_token)
    order_by = request.GET.get('order')
    if order_by == 'voted':
        msgs_query = queries.get_messages_by_voted()
    else:
        msgs_query = queries.get_messages_by_date()
    
    msgs_query = msgs_query.filter(thread__subject_token=thread_token)
    emails = msgs_query.exclude(id=first_message.id)
    
    total_votes = first_message.votes_count()
    for email in emails:
        total_votes += email.votes_count()

    # Update relevance score
    thread = Thread.objects.get(subject_token=thread_token)   
    thread.update_score()
 
    template_data = {
        'first_msg': first_message,
        'emails': [first_message] + list(emails),
        'pagehits': queries.get_page_hits(request.path_info),
        'total_votes': total_votes,
    }
    
    return render_to_response('message-thread.html', template_data, 
                              RequestContext(request))


def list_messages(request):
    
    selected_list = request.GET.get('list')

    order_by = request.GET.get('order')
    if order_by == 'hotest':
        threads = queries.get_hotest_threads()
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
        'selected_list': selected_list,
        'order_by': order_by,
    }
    return render_to_response('message-list.html', template_data, 
                              RequestContext(request))
