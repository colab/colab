
from fabric.operations import put
from fabric.api import run, sudo, env
from fabric.contrib.files import exists
from fabric.decorators import with_settings
from fabric.context_managers import prefix, cd, settings

env.user = 'colab'  # key depends on env
env.use_shell = False

environments = {
    'dev': {
        'hosts': ['127.0.0.1'],
        'key_filename': '~/.vagrant.d/insecure_private_key',
        'port': 2222,
    },
    'live': {
        'hosts': ['10.1.2.153'],
        'key_filename': '~/.ssh/id_rsa',
        'port': 22,
    },
    'demo': {
        'hosts': ['colab-demo.tracy.com.br'],
        'key_filename': '~/.ssh/id_rsa',
        'port': 22,
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

    if not exists('~/apache-solr-3.6.2/'):
        run('wget http://archive.apache.org/dist/lucene/solr/3.6.2/apache-solr-3.6.2.tgz')
        run('tar xzf apache-solr-3.6.2.tgz')
        run('rm apache-solr-3.6.2.tgz')

    with cd('~/apache-solr-3.6.2/example/solr/conf/'):
        if not exists('stopwords_en.txt'):
            run('cp stopwords.txt stopwords_en.txt')

    if env_created:
        update_requirements()

    sudo('supervisorctl reload', shell=False)


def update_requirements():
    with cd('~/colab'), prefix(WORKON_COLAB):
        run('pip install -U -r requirements.txt')


def deploy(update=False):

    with cd('~/colab/src/'), prefix(WORKON_COLAB):
        run('git pull')

    if update:
        update_requirements()

    with cd('~/colab/src/'), prefix(WORKON_COLAB):
        run('python manage.py syncdb')
        run('python manage.py migrate')
        run('python manage.py collectstatic --noinput')
        run('python manage.py build_solr_schema -f ~/apache-solr-3.6.2/example/solr/conf/schema.xml')

    sudo('supervisorctl restart all')


@with_settings(user='vagrant')
def rebuild_index(age=None, batch=None):
    with cd('/vagrant/src/'), prefix(WORKON_COLAB):
        age_arg = ''
        if age:
            age_arg = '--age={}'.format(age)

        batch_arg = ''
        if batch:
            batch_arg = '--batch-size={}'.format(batch)

        cmd = 'python manage.py rebuild_index {} {}'.format(age_arg, batch_arg)
        returnMessage = run(cmd)
        if 'error: [Errno 111] Connection refused' in returnMessage:
            print red("Please run fab solr to start solr first")
        else:
            print green("All the index were updated")


@with_settings(user='vagrant')
def solr_update_index():
    with cd('/vagrant/src/'), prefix(WORKON_COLAB):
        returnMessage = run('python manage.py update_index')
        if 'error: [Errno 111] Connection refused' in returnMessage:
            print red("Please run fab solr to start solr first")
        else:
            print green("All the index were updated")


@with_settings(user='vagrant')
def build_solr_schema():
    with cd('/vagrant/src/'), prefix(WORKON_COLAB):
        run('python manage.py build_solr_schema -f /tmp/schema.xml')

    with settings(user='colab'):
        run('cp /tmp/schema.xml ~/apache-solr-3.6.2/example/solr/conf/schema.xml')

    sudo('supervisorctl restart solr')


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


@with_settings(user='vagrant')
def solr(port=8983):
    with cd('/vagrant/src/'), prefix(WORKON_COLAB):
        run('cd ~/solr-4.6.1/example; java -jar start.jar -Djetty.port={}'.format(port))


@with_settings(user='vagrant')
def solr_rebuild_index():
    with cd('/vagrant/src/'), prefix(WORKON_COLAB):
        returnMessage = run('python manage.py rebuild_index')
        if 'error: [Errno 111] Connection refused' in returnMessage:
            print red("Please run fab solr to start solr first")
        else:
            print green("All the index were updated")


@with_settings(user='vagrant')
def install_solr_4_6():
    with cd('/vagrant/src/'), prefix(WORKON_COLAB):
        if not exists('~/solr-4.6.1'):
            run('wget https://archive.apache.org/dist/lucene/solr/4.6.1/solr-4.6.1.tgz -O /tmp/solr-4.6.1.tgz')
            run('tar xzf /tmp/solr-4.6.1.tgz -C /tmp/')
            run('cp -rf /tmp/solr-4.6.1 ~/solr-4.6.1')
            run('rm /tmp/solr-4.6.1')

    with cd('~/solr-4.6.1/example/solr/collection1/conf/'), prefix(WORKON_COLAB):
        if not exists('stopwords_en.txt'):
            run('cp stopwords.txt stopwords_en.txt')


@with_settings(user='vagrant')
def import_emails():
    with cd('/vagrant/src/'), prefix(WORKON_COLAB):
        run('python manage.py import_emails')


@with_settings(user='vagrant')
def solr_4_build_schema():
    with cd('/vagrant/src/'), prefix(WORKON_COLAB):
        solr_schema_file = '~/solr-4.6.1/example/solr/collection1/conf/schema.xml'
        run('python manage.py build_solr_schema -f {}'.format(solr_schema_file))
        run(r'sed -i "s/<fields>/<fields>\n<field name=\"_version_\" type=\"long\" indexed=\"true\" stored =\"true\"\/>/" {}'.format(solr_schema_file))


def red(message):
    return "\033[0;31m" + message + "\033[0m"


def green(message):
    return "\033[0;32m" + message + "\033[0m"
