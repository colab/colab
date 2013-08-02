
from fabric.api import run, sudo, env
from fabric.contrib.files import exists
from fabric.context_managers import prefix, cd
from fabric.decorators import with_settings

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


def install():
    if not exists('~colab/.virtualenvs/colab'):
        with prefix(SOURCE_VENV):
            run('mkvirtualenv colab')

    if not exists('~colab/colab'):
        run('git clone https://github.com/TracyWebTech/colab ~colab/colab')

    sudo('supervisorctl reload', shell=False        )


def deploy():
    with cd('~colab/colab'):
        run('git pull')

    with prefix(WORKON_COLAB):
        run('pip install -r ~colab/colab/requirements.txt')

