from django.utils.translation import ugettext_lazy as _

name = 'colab.plugins.gitlab'
verbose_name = 'Gitlab Proxy'

upstream = 'localhost'
#middlewares = []

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


#  dpaste:
#    dependencies:
#      - 'mptt'
#    urls:
#      include: 'dpaste.urls.dpaste'
#      prefix:  '^paste/'
#      namespace: 'dpaste'
#    menu:
#      title: 'Dpaste'
#      links:
#        Public Projects:  '/paste'
#      auth_links:
#        Profile: '/projects'
#        New Project: '/projects/new'
