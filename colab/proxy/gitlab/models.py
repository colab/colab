from django.db import models
from django.utils.translation import ugettext_lazy as _
from colab.proxy.utils.models import Collaboration


class GitlabProject(models.Model):

    id = models.IntegerField(primary_key=True)
    description = models.TextField()
    public = models.BooleanField(default=True)
    name = models.TextField()
    name_with_namespace = models.TextField()
    created_at = models.DateTimeField(blank=True)
    last_activity_at = models.DateTimeField(blank=True)

    class Meta:
        verbose_name = _('Gitlab Project')
        verbose_name_plural = _('Gitlab Projects')


class GitlabMergeRequest(Collaboration):

    id = models.IntegerField(primary_key=True)
    target_branch = models.TextField()
    source_branch = models.TextField()
    project = models.ForeignKey(GitlabProject, null=True,
                                on_delete=models.SET_NULL)
    description = models.TextField()
    title = models.TextField()
    state = models.TextField()

    class Meta:
        verbose_name = _('Gitlab Merge Request')
        verbose_name_plural = _('Gitlab Merge Requests')


class GitlabIssue(Collaboration):

    id = models.IntegerField(primary_key=True)
    project = models.ForeignKey(GitlabProject, null=True,
                                   on_delete=models.SET_NULL)
    title = models.TextField()
    description = models.TextField()

    state = models.TextField()

    class Meta:
        verbose_name = _('Gitlab Collaboration')
        verbose_name_plural = _('Gitlab Collaborations')


class GitlabComment(Collaboration):

    id = models.IntegerField(primary_key=True)
    body = models.TextField()
    created_at = models.DateTimeField(blank=True)

    class Meta:
        verbose_name = _('Gitlab Comments')
        verbose_name_plural = _('Gitlab Comments')
