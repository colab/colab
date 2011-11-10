
from django.contrib import admin
from super_archives.models import MailingList, MailingListMembership, \
                                  Message, MessageMetadata, Vote

admin.site.register(MailingList)
admin.site.register(MailingListMembership)
admin.site.register(Message)
admin.site.register(MessageMetadata)
admin.site.register(Vote)
