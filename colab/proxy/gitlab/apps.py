
from django.utils.translation import ugettext_lazy as _

from ..utils.apps import ColabProxiedAppConfig


class ProxyGitlabAppConfig(ColabProxiedAppConfig):
    '''
    You can define a collaboration_models list to tell colab which
    models and what values should be displayed as collaborations.

    See the example bellow:

    Field model refers to the model to be displayed.
    Field model_verbose is the human name to be displayed in charts.
    Field collaborator_username tells which user(username) is
        associated with this collaboration.

    The value of the hashes maps the attribute or method of the model
        to be put in those positions.

        collaboration_models = [
            {
                'model' : 'User',
                'model_verbose' : 'User',
                'tag' : '',
                'title' : 'username',
                'description' : 'get_full_name',
                'fullname' : '',
                'modified' : 'modified',
                'modified_by' : '',
                'modified_by_url' : '',
                'url' : '',
                'type' : '',
                'collaborator_username' : 'username',
            },
        ]
    '''
    name = 'colab.proxy.gitlab'
    verbose_name = 'Gitlab Proxy'

    menu = {
        'title': _('Code'),
        'links': (
            (_('Public Projects'), 'public/projects'),
        ),
        'auth_links': (
            (_('Profile'), 'profile'),
            (_('New Project'), 'projects/new'),
            (_('Projects'), 'dashboard/projects'),
            (_('Groups'), 'profile/groups'),
            (_('Issues'), 'dashboard/issues'),
            (_('Merge Requests'), 'dashboard/merge_requests'),

        ),
    }

    collaboration_models = []

