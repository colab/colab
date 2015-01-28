
from .models import Message


def mailarchive(request):
    context = {}

    try:
        context['last_imported_message'] = \
            Message.objects.latest('received_time')
    except Message.DoesNotExist:
        pass

    return context
