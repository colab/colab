from django.db import models
from django.utils import timezone


class TimeStampPlugin(models.Model):
    '''
        Class used to store timestamps from plugins
    '''
    name = models.CharField(max_length=255, unique=True, null=False)
    timestamp = models.DateTimeField(default=timezone.datetime.min, blank=True)

    @classmethod
    def update_timestamp(cls, class_name, **kwargs):
        instance = TimeStampPlugin.objects.get_or_create(name=class_name)[0]
        last_updated = kwargs.get('last_updated', '')

        if last_updated:
            format = "%Y/%m/%d %H:%M:%S"
            instance.timestamp = timezone.datetime.strptime(last_updated,
                                                            format)
        else:
            instance.timestamp = timezone.datetime.now()
        instance.save()

    @classmethod
    def get_last_updated(cls, class_name):
        instance = TimeStampPlugin.objects.get_or_create(name=class_name)[0]
        return instance.timestamp
