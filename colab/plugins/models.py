from django.db import models
from django.utils.timezone import datetime


class TimeStampPlugin(models.Model):
    '''
        Class used to store timestamps from plugins
    '''
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, null=False)
    timestamp = models.DateTimeField(default=datetime.min, blank=True)

    @classmethod
    def update_timestamp(cls, class_name, **kwargs):
        instance = TimeStampPlugin.objects.filter(name=class_name)[0]
        last_updated = kwargs.get('last_updated', '')

        if last_updated:
            instance.timestamp = datetime.strptime(last_updated,
                                                   "%Y/%m/%d %H:%M:%S")
        else:
            instance.timestamp = datetime.now()
        instance.save()

    @classmethod
    def get_last_updated(cls, class_name):
        instance = TimeStampPlugin.objects.get_or_create(name=class_name)[0]
        return instance.timestamp
