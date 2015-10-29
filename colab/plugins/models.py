from django.db import models
from datetime import datetime

class TimeStampPlugin(models.Model):
    '''
        Class used to store timestamp from plugins
    '''
    id = models.IntegerField(primary_key= True)
    name = models.CharField(max_length=255,unique=True,null=False)
    timestamp = models.DateTimeField(default=datetime.min,blank=True)
