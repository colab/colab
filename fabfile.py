

from fabric.operations import put
from fabric.api import run, sudo, env
from fabric.contrib.files import exists
from fabric.decorators import with_settings
from fabric.context_managers import prefix, cd

env.user = 'colab' # key depends on env
env.use_shell = False

environments = {
    'dev': {
        'hosts': ['127.0.0.1'],
        'port': 2222,
        'key_filename': '~/.vagrant.d/insecure_private_key',
    },
    'live': {
        'hosts': [], #TODO
        'key_filename': '~/.ssh/id_rsa',
    },
}


SOURCE_VENV = 'source /usr/local/bin/virtualenvwrapper.sh'
WORKON_COLAB = '{} && workon colab'.format(SOURCE_VENV)


def environment(name):
     env.update(environments[name])
     env.environment = name
environment('dev')


def mkvirtualenv():
    if not exists('~/.virtualenvs/colab'):
        with prefix(SOURCE_VENV):
            run('mkvirtualenv colab')
            return True


def install(local_settings=None):
    env_created = mkvirtualenv()

    if not exists('~/colab'):
        run('git clone https://github.com/TracyWebTech/colab ~/colab')

    if local_settings:
        put(local_settings, '~/colab/src/colab/local_settings.py')

    if env_created:
        update_requirements()

    sudo('supervisorctl reload', shell=False)


def update_requirements():
    with cd('~/colab'), prefix(WORKON_COLAB):
        run('pip install -r requirements.txt')


def deploy(update=False):
    if update:
        update_requirements()

    with cd('~/colab/src/'), prefix(WORKON_COLAB):
        run('git pull')
        run('python manage.py syncdb')
        run('python manage.py migrate')
        run('python manage.py collectstatic --noinput')

    sudo('supervisorctl restart all')


@with_settings(user='vagrant')
def runserver(update_requirements=False):
    env_created = mkvirtualenv()

    with cd('/vagrant/src/'), prefix(WORKON_COLAB):

        # If explicitly called or if it's a new environment
        if update_requirements or env_created:
            run('pip install -r /vagrant/requirements.txt')

        run('python manage.py syncdb')
        run('python manage.py migrate')
        run('python manage.py runserver 0.0.0.0:7000')
