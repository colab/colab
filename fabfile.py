# coding: utf-8

import os

from fabric import colors
from fabric.utils import error
from fabric.decorators import task
from fabric.api import env, run, sudo, local
from fabric.contrib.files import exists
from fabric.context_managers import prefix, cd, settings, shell_env

DEBIAN_FAMILY = ['debian', 'ubuntu']
REDHAT_FAMILY = ['centos', 'fedora']

DISTRO_CMD = {
    'debian': ('apt-get', {
        'install': '-y',
        'update': '-y',
        }),
    'redhat': ('yum', {
        'install': '-y',
        'update': '-y',
        })
}

APP_USER = APP_NAME = VENV_NAME = 'colab'
REPO_URL = 'git@github.com:colab-community/colab.git'


environments = {
    'dev': {
        'hosts': ['127.0.0.1'],
        'key_filename': '~/.vagrant.d/insecure_private_key',
        'port': 2222,
        'is_vagrant': True,
        'superuser': 'vagrant',
    },
}
DEFAULT_ENVIRONMENT = 'dev'

env.user = APP_USER
env.use_shell = False

PROJECT_PATH = os.path.join(os.path.dirname(__file__))
REPO_PATH = '/home/{}/{}'.format(APP_USER, APP_NAME)
SOURCE_VENV = 'source /usr/local/bin/virtualenvwrapper.sh'

WORKON_ENV = '{} && workon {}'.format(SOURCE_VENV, VENV_NAME)
MANAGE_PATH = os.path.join(REPO_PATH, 'src')
SETTINGS_PATH = os.path.join(MANAGE_PATH, APP_NAME)


def get_distro_family():
    cmd = 'python -c "import platform; print platform.dist()[0]"'
    linux_name = run(cmd).lower()
    if linux_name in DEBIAN_FAMILY:
        return 'debian'
    elif linux_name in REDHAT_FAMILY:
        return 'redhat'
    else:
        error(colors.red('Distribuiton `{}` not supported'.format(linux_name)))
        exit(1)


def cmd(family, command, args=''):
    pkgmanager, commands = DISTRO_CMD[family]
    return ' '.join([pkgmanager, command, commands[command], args])


@task
def environment(name=DEFAULT_ENVIRONMENT):
    """Set the environment where the tasks will be executed"""
    global REPO_URL

    try:
        import project_cfg
    except ImportError:
        pass
    else:
        REPO_URL = project_cfg.repository_url
        environments.update(project_cfg.environments)

    if name not in environments:
        error(colors.red('Environment `{}` does not exist.'.format(name)))

    env.update(environments[name])
    env.environment = name


def package_install(pkg):
    family = get_distro_family()
    sudo(cmd(family, 'install', pkg))


def install_requirements():
    with cd(REPO_PATH), prefix(WORKON_ENV):
        run('pip install -U distribute')
        if not env.is_vagrant:
            run('pip install -r requirements.txt')
            return

        if exists('requirements-{}.txt'.format(env.environment)):
            run('pip install -r requirements-{}.txt'.format(env.environment))
        else:
            run('pip install -r requirements.txt')


def mkvirtualenv():
    if not exists('~/.virtualenvs/' + VENV_NAME):

        with prefix(SOURCE_VENV):
            run('mkvirtualenv ' + VENV_NAME)
            return True


def manage(command):
    django_settings = env.get('django_settings')
    env_vars = {}
    if django_settings:
        env_vars.update({'DJANGO_SETTINGS_MODULE': django_settings})

    with shell_env(**env_vars):
        with cd(MANAGE_PATH), prefix(WORKON_ENV):
            run('python manage.py {}'.format(command))


def syncdb():
    manage('syncdb --no-initial-data')


def migrate():
    manage('migrate')
    manage('loaddata super_archives/fixture/initial_data.json')


def collectstatic():
    sudo('mkdir -p /usr/share/nginx/{}'.format(APP_NAME))
    sudo('chown {} /usr/share/nginx/{}'.format(env.user, APP_NAME))
    manage('collectstatic --noinput')


def create_local_settings():
    with cd(SETTINGS_PATH):
        env_local_settings = 'local_settings-{}.py'.format(env.environment)

        if not exists('local_settings.py') and exists(env_local_settings):
            run('ln -s {} {}'.format(env_local_settings, 'local_settings.py'))
            run('chown {} local_settings.py'.format(env.user))


def update_code():
    if env.is_vagrant:
        if not exists(REPO_PATH):
            run('ln -s /vagrant/ {}'.format(REPO_PATH))
        return

    if not exists(REPO_PATH):
        run('git clone {} {}'.format(REPO_URL, REPO_PATH))
    else:
        with cd(REPO_PATH):
            run('git pull')


@task
def bootstrap():
    """Bootstrap machine to run fabric tasks"""

    with settings(user=env.superuser):
        family = get_distro_family()
        if(family == 'debian'):
            sudo(cmd(family, 'update'))
        else:
            package_install('wget')

        if not exists('/usr/bin/git'):
            package_install('git-core')

        if env.is_vagrant:
            groups = ['sudo', 'vagrant']
            local('chmod -fR g+w {}'.format(PROJECT_PATH))
        else:
            groups = ['sudo']

        for group in groups:
            sudo('groupadd -f {}'.format(group))

        command = 'useradd {} -G {} -m -s /bin/bash'
        sudo(command.format(APP_USER, ','.join(groups)))

        ssh_dir = '/home/{0}/.ssh/'.format(APP_USER)
        if not exists(ssh_dir):
            sudo('mkdir -p {0}'.format(ssh_dir))
            sudo('chmod 700 {0}'.format(ssh_dir))
            sudo('cp ~{}/.ssh/authorized_keys /home/{}/.ssh/'.format(
                env.superuser,
                APP_USER
            ))
            sudo('chown -fR {0}:{0} {1}'.format(APP_USER, ssh_dir))

        sudoers_file = os.path.join('/etc/sudoers.d/', APP_USER)
        tmp_file = os.path.join('/tmp', APP_USER)
        if not exists(sudoers_file):
            sudo('echo "{} ALL=NOPASSWD: ALL" > {}'.format(APP_USER, tmp_file))
            sudo('chown root:root {}'.format(tmp_file))
            sudo('chmod 440 {}'.format(tmp_file))
            sudo('mv {} {}'.format(tmp_file, sudoers_file))


@task
def provision():
    """Run puppet"""

    update_code()

    puppet_path = os.path.join(REPO_PATH, 'puppet/')
    modules_path = os.path.join(puppet_path, 'modules')
    puppet_modules = '{}:/etc/puppet/modules'.format(modules_path)

    with cd(puppet_path):
        run('sudo python bootstrap.py')

    if env.is_vagrant:
        cmd = os.path.join(puppet_path, 'manifests', 'site.pp')
    else:
        cmd = '-e "include {}"'.format(APP_NAME)

    if not exists('/usr/bin/puppet'):
        print(colors.red('Please install `puppet` before continue.'))
        return

    sudo('puppet apply --modulepath={} {}'.format(puppet_modules, cmd))


@task
def ssh_keygen():
    """Create SSH credentials"""

    if not exists('~/.ssh/id_rsa'):
        run("ssh-keygen -f ~/.ssh/id_rsa -N '' -b 1024 -q")
    key = run('cat ~/.ssh/id_rsa.pub')

    print('Public key:')
    print(colors.yellow(key))
    print('')
    print('Add the key above to your github repository deploy keys')


@task
def deploy(noprovision=False):
    """Deploy and run the new code (master branch)"""

    if noprovision is False:
        provision()
    else:
        update_code()

    fix_path()

    install_solr()

    mkvirtualenv()

    sudo('supervisorctl stop all')

    install_requirements()
    create_local_settings()
    collectstatic()
    syncdb()
    migrate()

    build_schema()

    sudo('supervisorctl start all')


def fix_path():
    global SOURCE_VENV
    global WORKON_ENV
    if exists('/usr/bin/virtualenvwrapper.sh'):
        SOURCE_VENV = 'source /usr/bin/virtualenvwrapper.sh'
        WORKON_ENV = '{} && workon {}'.format(SOURCE_VENV, VENV_NAME)


@task
def install_solr():
    """Install Solr"""

    SOLR_PKG = 'https://archive.apache.org/dist/lucene/solr/4.6.1/solr-4.6.1.tgz'

    if not exists('~/solr-4.6.1'):
        run('wget {} -O /tmp/solr-4.6.1.tgz'.format(SOLR_PKG))
        run('tar xzf /tmp/solr-4.6.1.tgz -C /tmp/')
        run('cp -rf /tmp/solr-4.6.1 ~/solr-4.6.1')
        run('mv ~/solr-4.6.1/example ~/solr-4.6.1/colab')
        run('chmod +x ~/solr-4.6.1/colab/start.jar')
        run('rm /tmp/solr-4.6.1.tgz')

    with cd('~/solr-4.6.1/colab/solr/collection1/conf/'):
        if not exists('stopwords_en.txt'):
            run('cp stopwords.txt stopwords_en.txt')


@task
def solr(port=8983):
    """Start Solr"""
    with cd('~/solr-4.6.1/colab'), settings(user='colab'):
        run('java -jar start.jar -Djetty.port={}'.format(port))


@task
def rebuild_index(age=None, batch=None):
    """Rebuild the solr index"""
    age_arg = ''
    if age:
        age_arg = '--age={}'.format(age)

    batch_arg = ''
    if batch:
        batch_arg = '--batch-size={}'.format(batch)

    manage('rebuild_index {} {}'.format(age_arg, batch_arg))


@task
def update_index():
    """Update solr index"""
    manage('update_index')


@task
def build_schema():
    """Build solr schema"""
    solr_schema_file = '~/solr-4.6.1/colab/solr/collection1/conf/schema.xml'
    manage('build_solr_schema -f {}'.format(solr_schema_file))
    run(r'sed -i "s/<fields>/<fields>\n<field name=\"_version_\" type=\"long\" indexed=\"true\" stored =\"true\"\/>/" {}'.format(solr_schema_file))


# Main
environment()
