
from django.contrib import admin
from .models import MailingList, Message, Thread, EmailAddress


class EmailAddressAdmin(admin.ModelAdmin):
    search_fields = (
        'address',
        'user__username',
        'user__first_name',
        'user__last_name',
    )


class MessageAdmin(admin.ModelAdmin):
    list_filter = ('spam', 'thread__mailinglist', 'received_time', )
    search_fields = (
        'id',
        'subject',
        'subject_clean',
        'body',
        'from_address__real_name',
        'from_address__address',
        'from_address__user__first_name',
        'from_address__user__last_name',
        'from_address__user__username',
    )
    readonly_fields = ('thread', 'from_address', 'mailinglist')


class ThreadAdmin(admin.ModelAdmin):
    list_filter = ('spam', 'mailinglist', 'message__received_time',)
    search_fields = (
        'id',
        'subject_token',
        'message__subject',
        'message__subject_clean',
        'message__from_address__real_name',
        'message__from_address__address',
        'message__from_address__user__first_name',
        'message__from_address__user__last_name',
        'message__from_address__user__username',
    )

    readonly_fields = (
        'mailinglist',
        'subject_token',
        'latest_message',
        'score',
    )

    fields = (
        'mailinglist',
        'subject_token',
        'latest_message',
        'score',
        'spam',
    )


admin.site.register(MailingList)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(EmailAddress, EmailAddressAdmin)
