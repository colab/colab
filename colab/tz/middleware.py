
import pytz

from django.utils import timezone


class TimezoneMiddleware(object):
    def process_request(self, request):
        offset = request.COOKIES.get('utc_offset', 0)

        try:
            offset = int(offset) * -1
            tz = pytz.FixedOffset(offset)
        except ValueError:
            offset = 0

        if offset:
            timezone.activate(tz)
        else:
            timezone.deactivate()
