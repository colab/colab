#!/usr/bin/env python
# encoding: utf-8

import math
import json
import urllib
import socket
import logging
import httplib

from dateutil.parser import parse as parse_timestamp

from django.conf import settings

from super_archives.models import EmailAddress


def build_query(user_query, filters=None):
    """Build the query that will be sent to Solr"""    

    if not user_query:
        user_query = '*'

    query = settings.SOLR_BASE_QUERY.strip() + ' AND ' + user_query
    if filters:
        query = "(%s)" % query

        for (key, value) in filters.items():
            if value:
                query += " AND %s:%s" % (key, value)
    
    logging.info(query)
    return query.encode('utf-8')


def parse_document_timestamps(doc, date_attrs=('modified', 'created')):
    """Converts the `modified' and `created' dates from
    ISO 8601 format to a date time object for the given 
    document.
    
    """
    
    for date in date_attrs:
        date_str = doc.get(date)
        try:
            date_obj = parse_timestamp(date_str)
        except ValueError:
            logging.error('Error trying to parse "%s"', date_str)
            date_obj = None
        doc.update({date: date_obj})
    
    return doc


def get_document_url(doc):
    """Set the url attribute for a document using the path_string.
    In case the resource comes from an external domain it will
    be prepended to this URL.

    """
    doc_type = doc.get('Type')
    
    url = ''
    if settings.SOLR_COLAB_URI:
        url += settings.SOLR_COLAB_URI
    
    url += doc.get('path_string', '') 
    doc.update({'url': url})
    
    return doc
    

def get_document_from_addr(doc):
    """Get a EmailAddress instance for the given document if 
    its available.
    
    """
    
    username = doc.get('last_author')
    if not username:
        username = doc.get('Creator')
    from_addresses = EmailAddress.objects.filter(user__username=username)
    if username and from_addresses:
        doc.update({'from_address': from_addresses[0]})
    

def add_attrs_to_doc(doc):
    """Wraps the call of functions that adds or modifies keys
    of the giving doc (which should be a dict).
    
    """
    get_document_url(doc)
    parse_document_timestamps(doc)
    get_document_from_addr(doc)


class SolrPaginator(list):
    
    def __init__(self, response_dict, current_page):
        super(SolrPaginator, self).__init__()
        
        responseHeader = response_dict.get('responseHeader', {}) 
        response = response_dict.get('response', {})
        request_params = responseHeader.get('params', {})
        
        docs = response.get('docs', [])
        self.extend(docs)

        self.QTime = int(responseHeader.get('QTime', 1)) / 1000.0
       
        self.per_page = int(request_params.get('rows', 10))
        self.numFound = int(response.get('numFound', 0))
        self.page_num = current_page
    
        self.num_of_pages = int(math.ceil(self.numFound / float(self.per_page)))
        
        self.has_previous = self.page_num > 1
        if self.has_previous: 
            self.previous_page_number = self.page_num - 1
        else:
            self.previous_page_number = None
        
        self.has_next = self.page_num < self.num_of_pages
        if self.has_next:
            self.next_page_number = self.page_num + 1        
        else:
            self.next_page_number = None
    
    @property
    def last_page(self):
        return self.num_of_pages


def select(query, results_per_page=None, page_number=None, sort=None, fields=None, link_attrs=True):
    """Perform a select in a Solr instance using the configuration
    set in settings.py.
    
    """
    
    data = {
        'q': query, 
        'wt': 'json',
    }
    
    # Number of results per page
    if results_per_page:
        data.update({'rows': results_per_page})
        
        # Page number
        if page_number:
            data.update({
                'start': (page_number - 1) * results_per_page,
            })
            
    # Sort order
    if sort:
        data.update({
            'sort': sort,
        })
    
    # Only select those fields
    if fields:
        data.update({
            'fl': ','.join(fields),
        })
    # First version of this was implemented using urllib2 and was
    #   a milion times easier but unfortunatelly urllib2.urlopen
    #   does not support http headers. Without setting http headers
    #   for charset the solr server tries to decode utf-8 params
    #   as ASCII causing it to crash. HTTPConnection deals with
    #   encodings automagically.
    solr_conn = httplib.HTTPConnection(settings.SOLR_HOSTNAME,          
                                       settings.SOLR_PORT)
    query_params = urllib.urlencode(data)
    solr_select_uri = settings.SOLR_SELECT_PATH + '?' + query_params
   
    # Socks proxy configuration. Only required for development
    #   if the solr server is behind a firewall. 
    socks_server = getattr(settings, "SOCKS_SERVER", None)
    if socks_server: 
        import socks
        logging.debug('Socks enabled: %s:%s', settings.SOCKS_SERVER,
                                              settings.SOCKS_PORT)

        socks.setdefaultproxy(settings.SOCKS_TYPE, 
                              settings.SOCKS_SERVER,
                              settings.SOCKS_PORT)
        socket.socket = socks.socksocket

    try:
        solr_conn.request('GET', solr_select_uri)
        solr_response = solr_conn.getresponse()
    except socket.error as err: 
        solr_response = None
        logging.exception(err)

    if solr_response and solr_response.status == 200:
        #TODO: Log error connecting to solr
        solr_json_resp = solr_response.read()
        solr_dict_resp = json.loads(solr_json_resp)
    else:
        solr_dict_resp = {}
    
    docs = solr_dict_resp.get('response', {}).get("docs", [])

    if link_attrs:
        # Loop over all documents adding or linking its information
        #   with the data from this app or database
        map(add_attrs_to_doc, docs)
    
    return solr_dict_resp
    

def get_latest_collaborations(number=10, username=None):
    """Get the n documents recently modified that this username
    has helped in somehow.
    
    """
    
    if username:
        filters = {'collaborator': username}
    else:
        filters = None
    
    query = build_query('*', filters)
    solr_response = select(
        query=query, 
        results_per_page=number, 
        sort='modified desc'
    )
    
    return solr_response.get('response', {}).get('docs', [])


def count_types(sample=100, filters=None):
    """Count the type of the last modifications returning the
    results in dict.
    
    Example: {
        'wiki' 30,
        'thread': 40,
        'ticket', 10,
        'changeset' 20,
    }
    
    """
    
    query = build_query('*', filters)
    solr_response = select(
        query=query,
        results_per_page=sample,
        sort='modified desc',
        link_attrs=False,
    )

    docs = solr_response.get('response', {}).get('docs', [])

    type_count = {}
    for doc in docs:
        doc_type = doc.get('Type')
        count = type_count.get(doc_type, 0) + 1
        type_count.update({doc_type: count})

    return type_count
    
    
