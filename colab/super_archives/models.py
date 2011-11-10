# -*- coding: utf8 -*-

from hashlib import md5

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class EmailAddress(models.Model):
    user = models.ForeignKey(User, null=True, related_name='emails') 
    address = models.EmailField(unique=True)
    real_name = models.CharField(max_length=64, blank=True)
    md5 = models.CharField(max_length=32, null=True)
        
    def save(self, *args, **kwargs):
        self.md5 = md5(self.address).hexdigest()
        super(EmailAddress, self).save(*args, **kwargs)
        
    def get_full_name(self):
        if self.user and self.user.get_full_name():
            return self.user.get_full_name()
        elif self.user and self.username:
            return self.username
        elif self.real_name:
            return self.real_name
            
    def get_profile_link(self):
        if self.user:
            return reverse('colab.views.user_profile_username',
                           args=[self.user.username])
        else:
            return reverse('colab.views.user_profile_emailhash',
                           args=[self.md5])


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    institution = models.CharField(max_length=128, null=True)
    role = models.CharField(max_length=128, null=True)
    twitter = models.CharField(max_length=128, null=True)
    facebook = models.CharField(max_length=128, null=True)
    google_talk = models.EmailField(null=True)
    webpage = models.CharField(max_length=256)

# This does the same the same than related_name argument but it also creates
#   a profile in the case it doesn't exist yet. 
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class MailingList(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    description = models.TextField()
    logo = models.FileField(upload_to='list_logo') #TODO
    last_imported_index = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class MailingListMembership(models.Model):
    user = models.ForeignKey(User)
    mailinglist = models.ForeignKey(MailingList)

    def __unicode__(self):
        return '%s on %s' % (self.user.username, self.mailinglist.name)


class Thread(models.Model):
    subject_token = models.CharField(max_length=512)
    mailinglist = models.ForeignKey(MailingList)
    latest_message = models.OneToOneField('Message', null=True, 
                                                     related_name='+')           
    class Meta:
        unique_together = ('subject_token', 'mailinglist')


class Vote(models.Model):
    user = models.ForeignKey(User)
    message = models.ForeignKey('Message')

    class Meta:
        unique_together = ('user', 'message')

    def __unicode__(self):
        return 'Vote on %s by %s' % (self.Message.id,
                                     self.user.username)


class Message(models.Model):
    
    from_address = models.ForeignKey(EmailAddress)
    mailinglist = models.ForeignKey(MailingList)
    thread = models.ForeignKey(Thread, null=True)
    # RFC 2822 recommends to use 78 chars + CRLF (so 80 chars) for
    #   the max_length of a subject but most of implementations
    #   goes for 256. We use 512 just in case.
    subject = models.CharField(max_length=512)
    subject_clean = models.CharField(max_length=512)
    body = models.TextField(default='')
    received_time = models.DateTimeField()
    message_id = models.CharField(max_length=512)

    def __unicode__(self):
        return 'Email Message Id: %s' % self.id
        
    def vote_list(self):
        """Return a list of user that voted in this message."""
        
        return [vote.user for vote in self.vote_set.all()]        
 
    def votes_count(self):
        return len(self.vote_list())
        
    def vote(self, user):
        Vote.objects.create(
            message=self,
            user=user
        )
        
    def unvote(self, user):
        Vote.objects.get(
            message=self,
            user=user
        ).delete()
        

class MessageMetadata(models.Model):
    Message = models.ForeignKey(Message)
    # Same problem here than on subjects. Read comment above
    #   on Message.subject
    name = models.CharField(max_length=512)
    value = models.TextField()

    def __unicode__(self):
        return 'Email Message Id: %s - %s: %s' % (self.Message.id,
                                                  self.name, self.value)

