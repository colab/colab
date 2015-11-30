
import re

from django.utils.html import strip_tags

from html2text import html2text


EXTENDED_PUNCTUATION = '!"#$%&\'()*+,-./:;=?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
RE_WRAPPED_BY_HTML = re.compile(r'^<[a-z]+[^>]*>.*</[a-z]+[^>]*>$',
                                re.MULTILINE | re.IGNORECASE | re.DOTALL)
RE_LINKS = re.compile(r'(?P<link>https?://[^ \t\r\n\<]+)')
LINK_MARKUP = u'<a target="_blank" href="\g<link>">\g<link></a>'

RE_REPLY_LINE = re.compile(r'^[\s\t>]*>[\s\t]*')

RE_BR_TO_LINEBREAK = re.compile(r'<\s*/?\s*br\s*/?\s*>')


class EmailBlock(list):
    def __init__(self, is_reply=False, mark_links=True, html2text=True):
        self.mark_links = mark_links
        self.html2text = html2text
        self.is_reply = is_reply

    def _html2text(self, text):
        if RE_WRAPPED_BY_HTML.match(text.strip()):
            return html2text(text).strip()

        text, n = RE_BR_TO_LINEBREAK.subn('\n', text)
        text = strip_tags(text)
        return text

    def _mark_links(self, text):
        text, n = RE_LINKS.subn(LINK_MARKUP, text)
        return text

    @property
    def text(self):
        block = u''.join(self)

        if self.html2text:
            block = self._html2text(block)

        if self.mark_links:
            block = self._mark_links(block)

        return block

    def __unicode__(self):
        return self.text

    def __str__(self):
        return self.text


class EmailBlockParser(list):
    def __init__(self, email):
        self.email = email
        self.thread_emails = email.thread.message_set

        message = email.body
        block = EmailBlock()

        for line in message.split('\n'):
            if self.context_switch(line, block):
                self.append(block)
                new_block_context = not block.is_reply
                block = EmailBlock(is_reply=new_block_context)

            block.append(line + '\n')

        self.append(block)

    def context_switch(self, line, block):
        if line.strip(EXTENDED_PUNCTUATION):
            if self.is_reply(line):
                if not block.is_reply:
                    return True

            else:
                if block.is_reply:
                    return True

        return False

    def is_reply(self, line):
        stripped_line = line.strip()
        if stripped_line.startswith('>') or RE_REPLY_LINE.match(line):
            return True

        clean_line = RE_REPLY_LINE.subn('', stripped_line)[0]
        queryset = \
            self.thread_emails.filter(
                received_time__lt=self.email.received_time,
                body__contains=clean_line).order_by('-received_time')

        if queryset[:1]:
            return True

        return False
