# -*- coding: utf-8 -*-

import math
import string

from django.template import loader, Context
from django.utils.text import slugify
from haystack import indexes
from haystack.utils import log as logging

from search.base_indexes import BaseIndex
from .models import Attachment, Ticket, Wiki, Revision


logger = logging.getLogger('haystack')

# the string maketrans always return a string encoded with latin1
# http://stackoverflow.com/questions/1324067/how-do-i-get-str-translate-to-work-with-unicode-strings
table = string.maketrans(
    string.punctuation,
    '.' * len(string.punctuation)
).decode('latin1')


class AttachmentIndex(BaseIndex, indexes.Indexable):
    title = indexes.CharField(model_attr='filename')
    description = indexes.CharField(model_attr='description', null=True)
    modified = indexes.DateTimeField(model_attr='created', null=True)
    used_by = indexes.CharField(model_attr='used_by', null=True, stored=False)
    mimetype = indexes.CharField(
        model_attr='mimetype',
        null=True,
        stored=False
    )
    size = indexes.IntegerField(model_attr='size', null=True, stored=False)
    filename = indexes.CharField(stored=False)

    def get_model(self):
        return Attachment

    def get_updated_field(self):
        return 'created'

    def prepare(self, obj):
        data = super(AttachmentIndex, self).prepare(obj)

        try:
            file_obj = open(obj.filepath)
        except IOError as e:
            logger.warning(u'IOError: %s - %s', e.strerror, e.filename)
            return data
        backend = self._get_backend(None)

        extracted_data = backend.extract_file_contents(file_obj)
        file_obj.close()

        if not extracted_data:
            return data

        t = loader.select_template(
            ('search/indexes/proxy/attachment_text.txt', )
        )
        data['text'] = t.render(Context({
            'object': obj,
            'extracted': extracted_data,
        }))
        return data

    def prepare_filename(self, obj):
        return obj.filename.translate(table).replace('.', ' ')

    def prepare_icon_name(self, obj):
        return u'file'

    def prepare_type(self, obj):
        return u'attachment'


class WikiIndex(BaseIndex, indexes.Indexable):
    title = indexes.CharField(model_attr='name')
    collaborators = indexes.CharField(
        model_attr='collaborators',
        null=True,
        stored=False,
    )

    def get_model(self):
        return Wiki

    def prepare_description(self, obj):
        return u'{}\n{}'.format(obj.wiki_text, obj.collaborators)

    def prepare_icon_name(self, obj):
        return u'book'

    def prepare_type(self, obj):
        return u'wiki'


class TicketIndex(BaseIndex, indexes.Indexable):
    tag = indexes.CharField(model_attr='status', null=True)
    milestone = indexes.CharField(model_attr='milestone', null=True)
    component = indexes.CharField(model_attr='component', null=True)
    severity = indexes.CharField(model_attr='severity', null=True)
    reporter = indexes.CharField(model_attr='reporter', null=True)
    keywords = indexes.CharField(model_attr='keywords', null=True)
    collaborators = indexes.CharField(
        model_attr='collaborators',
        null=True,
        stored=False,
    )

    def get_model(self):
        return Ticket

    def prepare_description(self, obj):
        return u'{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(
            obj.description, obj.milestone, obj.component, obj.severity,
            obj.reporter, obj.keywords, obj.collaborators
        )

    def prepare_icon_name(self, obj):
        return u'tag'

    def prepare_title(self, obj):
        return u'#{} - {}'.format(obj.pk, obj.summary)

    def prepare_type(self, obj):
        return 'ticket'


class RevisionIndex(BaseIndex, indexes.Indexable):
    description = indexes.CharField(model_attr='message', null=True)
    modified = indexes.DateTimeField(model_attr='created', null=True)
    repository_name = indexes.CharField(
        model_attr='repository_name',
        stored=False
    )

    def get_model(self):
        return Revision

    def get_updated_field(self):
        return 'created'

    def get_boost(self, obj):
        boost = super(RevisionIndex, self).get_boost(obj)
        return boost * 0.8

    def prepare_icon_name(self, obj):
        return u'align-right'

    def prepare_title(self, obj):
        return u'{} [{}]'.format(obj.repository_name, obj.rev)

    def prepare_type(self, obj):
        return 'changeset'
