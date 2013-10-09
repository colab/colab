
import re

from django import template
from django.core.cache import cache

from html2text import html2text


register = template.Library()
TEMPLATE_PATH = 'superarchives/tags/'


EXTENDED_PUNCTUATION = '!"#$%&\'()*+,-./:;=?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
RE_WRAPPED_BY_HTML = re.compile(r'^<[a-z]+[^>]*>.*</[a-z]+[^>]*>$',
                                re.MULTILINE|re.IGNORECASE|re.DOTALL)
RE_LINKS = re.compile(r'(?P<link>https?://[^ \t\r\n\<]+)')


def find_links(block):
    links = RE_LINKS.finditer(block)

    block, n = RE_LINKS.subn(r'<a target="_blank" href="\g<link>">\g<link></a>',
                             block)

    return block


def join(block):
    block_txt = u''.join(block)

    if RE_WRAPPED_BY_HTML.match(block_txt.strip()):
        block = html2text(block_txt)
    else:
        block = block_txt

    return find_links(block)

def is_reply(line, message, thread):
    clean_line = line.strip()
    if clean_line.startswith('>'):
        return True

    for other_msg in thread:
        if other_msg == message:
            return False

        clean_body = other_msg.body.replace('\r', ' ')\
                                   .replace('\n', ' ')
        if clean_line.strip('> ') in clean_body:
            return True

    return False


@register.inclusion_tag(TEMPLATE_PATH + 'display_message.html')
def display_message(email, thread):
    message = email.body
    messages = []

    block = []
    reply_block = False

    for line in message.split('\n'):
        if line.strip(EXTENDED_PUNCTUATION):
            if is_reply(line, email, thread):
                if not reply_block:
                    reply_block = True
                    messages.append((join(block), 'normal'))
                    block = []
            elif reply_block:
                reply_block = False
                messages.append((join(block), 'reply'))
                block = []

        block.append(line.rstrip() + '\n')

    if reply_block:
        messages.append((join(block), 'reply'))
    else:
        messages.append((join(block), 'normal'))

    return {'messages': messages,
            'cache_key': email.pk,
            'cache_timeout': cache.default_timeout}
