#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Import emails from a mailman storage to the django database."""

import os
import re
import sys
import mailbox
import logging
from optparse import make_option

from django.conf import settings
from django.db import transaction
from django.template.defaultfilters import slugify
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from colab.super_archives.utils.email import colab_send_email
from colab.super_archives.models import (MailingList, Message,
                                         Thread, EmailAddress)
from message import Message as CustomMessage


class Command(BaseCommand, object):
    """Get emails from mailman archives and import them in the django db. """

    help = __doc__

    RE_SUBJECT_CLEAN = re.compile('((re|res|fw|fwd|en|enc):)|\[.*?\]',
                                  re.IGNORECASE)
    THREAD_CACHE = {}
    EMAIL_ADDR_CACHE = {}

    lock_file = settings.SUPER_ARCHIVES_LOCK_FILE

    # A new command line option to get the dump file to parse.
    option_list = BaseCommand.option_list + (
        make_option(
            '--archives_path',
            dest='archives_path',
            help=('Path of email archives to be imported. '
                  '(default: {})').format(settings.SUPER_ARCHIVES_PATH),
            default=settings.SUPER_ARCHIVES_PATH),

        make_option(
            '--exclude-list',
            dest='exclude_lists',
            help=("Mailing list that won't be imported. It can be used many"
                  "times for more than one list."),
            action='append',
            default=settings.SUPER_ARCHIVES_EXCLUDE),

        make_option(
            '--all',
            dest='all',
            help='Import all messages (default: False)',
            action="store_true",
            default=False),
    )

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def log(self, msg, error=False):
        """Log message helper."""
        output = self.stdout
        if error:
            output = self.stderr

        output.write(msg)
        output.write('\n')

    def parse_emails(self, email_filename, index=0):
        """Generator function that parse and extract emails from the file
        `email_filename` starting from the position `index`.

        Yield: An instance of `mailbox.mboxMessage` for each email in the
        file.

        """
        self.log("Parsing email dump: %s." % email_filename)
        mbox = mailbox.mbox(email_filename, factory=CustomMessage)

        # Get each email from mbox file
        #
        #   The following implementation was used because the object
        #   mbox does not support slicing. Converting the object to a
        #   tuple (as represented in the code down here) was a valid
        #   option but its performance was too poor.
        #
        # for message in tuple(mbox)[index:]:
        #     yield message
        #
        key = index
        while key in mbox:
            key += 1
            yield key-1, mbox[key-1]

    def get_emails(self, mailinglist_dir, all, exclude_lists):
        """Generator function that get the emails from each mailing
        list dump dirctory. If `all` is set to True all the emails in the
        mbox will be imported if not it will just resume from the last
        message previously imported. The lists set in `exclude_lists`
        won't be imported.

        Yield: A tuple in the form: (mailing list name, email message).

        """
        self.log("Getting emails dumps from: %s" % mailinglist_dir)

        # Get the list of directories ending with .mbox
        mailing_lists_mboxes = (mbox for mbox in os.listdir(mailinglist_dir)
                                if mbox.endswith('.mbox'))

        # Get messages from each mbox
        for mbox in mailing_lists_mboxes:
            mbox_path = os.path.join(mailinglist_dir, mbox, mbox)
            mailinglist_name = os.path.splitext(mbox)[0]

            # Check if the mailinglist is set not to be imported
            if exclude_lists and mailinglist_name in exclude_lists:
                continue

            # Find the index of the last imported message
            if all:
                n_msgs = 0
            else:
                try:
                    mailinglist = MailingList.objects.get(
                        name=mailinglist_name
                    )
                    n_msgs = mailinglist.last_imported_index
                except MailingList.DoesNotExist:
                    n_msgs = 0

            for index, msg in self.parse_emails(mbox_path, n_msgs):
                yield mailinglist_name, msg, index

    def get_thread(self, email, mailinglist):
        """Group messages by thread looking for similar subjects"""

        subject_slug = slugify(email.subject_clean)
        thread = self.THREAD_CACHE.get(subject_slug, {}).get(mailinglist.id)
        if thread is None:
            thread = Thread.all_objects.get_or_create(
                mailinglist=mailinglist,
                subject_token=subject_slug
            )[0]

            if self.THREAD_CACHE.get(subject_slug) is None:
                self.THREAD_CACHE[subject_slug] = dict()
            self.THREAD_CACHE[subject_slug][mailinglist.id] = thread

        thread.latest_message = email
        thread.update_keywords()
        thread.save()
        return thread

    def save_email(self, list_name, email_msg, index):
        """Save email message into the database."""

        msg_id = email_msg.get('Message-ID')
        if not msg_id:
            return

        # Update last imported message into the DB
        mailinglist, created = MailingList.objects.get_or_create(
            name=list_name
        )
        mailinglist.last_imported_index = index

        if created:
            # if the mailinglist is newly created it's sure that the message
            #   is not in the DB yet.
            self.create_email(mailinglist, email_msg)

        else:
            # If the message is already at the database don't do anything
            try:
                Message.all_objects.get(
                    message_id=msg_id,
                    thread__mailinglist=mailinglist
                )

            except Message.DoesNotExist:
                self.create_email(mailinglist, email_msg)

        mailinglist.save()

    def create_email(self, mailinglist, email_msg):
        received_time = email_msg.get_received_datetime()
        if not received_time:
            return

        real_name, from_ = email_msg.get_from_addr()

        email_addr = self.EMAIL_ADDR_CACHE.get(from_)
        if email_addr is None:
            email_addr = EmailAddress.objects.get_or_create(
                address=from_)[0]
            self.EMAIL_ADDR_CACHE[from_] = email_addr

        if not email_addr.real_name and real_name:
            email_addr.real_name = real_name[:64]
            email_addr.save()

        subject = email_msg.get_subject()
        if not subject:
            colab_send_email(
                subject=_(
                    u"[Colab] Warning - Email sent with a blank subject."
                ),
                message=render_to_string(
                    u'superarchives/emails/email_blank_subject.txt',
                    {
                        'email_body': email_msg.get_body(),
                        'mailinglist': mailinglist.name,
                        'user': email_addr.get_full_name()
                    }
                ),
                to=email_addr.address
            )

        email = Message.all_objects.create(
            message_id=email_msg.get('Message-ID'),
            from_address=email_addr,
            subject=subject,
            subject_clean=self.RE_SUBJECT_CLEAN.sub('', subject).strip(),
            body=email_msg.get_body(),
            received_time=email_msg.get_received_datetime(),
        )
        email.thread = self.get_thread(email, mailinglist)
        email.save()
        email.update_blocks()

    @transaction.commit_manually
    def import_emails(self, archives_path, all, exclude_lists=None):
        """Get emails from the filesystem from the `archives_path`
        and store them into the database. If `all` is set to True all
        the filesystem storage will be imported otherwise the
        importation will resume from the last message previously
        imported. The lists set in `exclude_lists` won't be imported.

        """

        count = 0
        email_generator = self.get_emails(archives_path, all, exclude_lists)
        for mailinglist_name, msg, index in email_generator:
            try:
                self.save_email(mailinglist_name, msg, index)
            except:
                # This anti-pattern is needed to avoid the transations to
                #   get stuck in case of errors.
                transaction.rollback()
                raise

            count += 1
            if count % 1000 == 0:
                transaction.commit()

        transaction.commit()

    def handle(self, *args, **options):
        """Main command method."""

        # Already running, so quit
        if os.path.exists(self.lock_file):
            self.log(("This script is already running. "
                      "(If your are sure it's not please "
                      "delete the lock file in {}')").format(self.lock_file))
            sys.exit(0)

        if not os.path.exists(os.path.dirname(self.lock_file)):
            os.mkdir(os.path.dirname(self.lock_file), 0755)

        archives_path = options.get('archives_path')
        self.log('Using archives_path `%s`' % settings.SUPER_ARCHIVES_PATH)

        if not os.path.exists(archives_path):
            msg = 'archives_path ({}) does not exist'.format(archives_path)
            raise CommandError(msg)
        run_lock = file(self.lock_file, 'w')
        run_lock.close()

        try:
            self.import_emails(
                archives_path,
                options.get('all'),
                options.get('exclude_lists'),
            )
        except Exception as e:
            logging.exception(e)
            raise
        finally:
            os.remove(self.lock_file)

        for mlist in MailingList.objects.all():
            mlist.update_privacy()
            mlist.save()
