
import pytz

from django.utils import timezone


class TimezoneMiddleware(object):
    def process_request(self, request):
        offset = request.COOKIES.get('utc_offset', 0)

        try:
            offset = int(offset) * -1
        except ValueError:
            offset = 0

        if offset:
            tz = pytz.FixedOffset(offset)
            timezone.activate(tz)
        else:
            timezone.deactivate()
