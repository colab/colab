
import re
import pytz
import email
import codecs
import mailbox
import datetime
from email.iterators import typed_subpart_iterator

import chardet


def get_charset(message, default='ASCII'):
    """Get the message charset"""

    charset = message.get_content_charset()

    if not charset:
        charset = message.get_charset()

    if not charset:
        charset = default

    try:
        codecs.lookup(charset)
    except LookupError:
        charset = default

    return charset


class Message(mailbox.mboxMessage):

    RECEIVED_DELIMITER = re.compile('\n|;')

    def get_subject(self):
        subject = email.header.decode_header(self['Subject'])

        if isinstance(subject, list):
            new_subject = u''
            for text_part, encoding in subject:
                if not encoding:
                    encoding = get_charset(self)

                try:
                    new_subject += unicode(text_part, encoding)
                except (UnicodeDecodeError, LookupError):
                    try:
                        new_subject += unicode(text_part, get_charset(self))
                    except (UnicodeDecodeError, LookupError):
                        encoding = chardet.detect(text_part)['encoding']
                        new_subject += unicode(text_part, encoding)

        return ''.join(new_subject)

    def get_body(self):
        """Get the body of the email message"""

        if self.is_multipart():
            # get the plain text version only
            text_parts = [part
                          for part in typed_subpart_iterator(self,
                                                             'text',
                                                             'plain')]
            body = []
            for part in text_parts:
                charset = get_charset(part, get_charset(self))
                body.append(unicode(part.get_payload(decode=True),
                                    charset,
                                    "replace"))

            return u"\n".join(body).strip()

        else:   # if it is not multipart, the payload will be a string
                # representing the message body
            body = unicode(self.get_payload(decode=True),
                           get_charset(self),
                           "replace")
            return body.strip()

    def get_received_datetime(self):
        if 'Received' not in self:
            return None
        # The time received should always be the last element
        #   in the `Received` attribute from the message headers
        received_header = self.RECEIVED_DELIMITER.split(self['Received'])
        received_time_header = received_header[-1].strip()

        date_tuple = email.utils.parsedate_tz(received_time_header)
        utc_timestamp = email.utils.mktime_tz(date_tuple)
        utc_datetime = datetime.datetime.fromtimestamp(utc_timestamp,
                                                       pytz.utc)

        return utc_datetime

    def get_from_addr(self):
        real_name_raw, from_ = email.utils.parseaddr(self['From'])
        real_name_str, encoding = email.header.decode_header(real_name_raw)[0]
        if not encoding:
            encoding = 'ascii'

        real_name = unicode(real_name_str, encoding, errors='replace')
        return real_name, from_
