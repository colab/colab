
class colab (
  $mailman_archive_path = 'default',
  $mailman_exclude_lists = [],
  $hostnames = [],
  $solr_project_path = '',
){

  require pip
  require appdeploy::deps::python
  require appdeploy::deps::essential
  require appdeploy::deps::openssl

  include ntp
  include security_updates
  include appdeploy::deps::lxml
  include appdeploy::deps::postgresql
  include colab::cronjobs
  include postgresql::globals
  include postgresql::server

  user { 'colab':
    gid    => 'colab',
    groups => ['sudo', 'mailman'],
    managehome => true,
  }

  group { 'mailman':
    ensure => present,
    system => true,
    before => User['colab'],
  }

  postgresql::server::db { 'colab':
    user     => 'colab',
    password => 'colab',
    grant    => 'all',
  }

  appdeploy::django { 'colab':
    user      => 'colab',
    directory => '/home/colab/',
    proxy_hosts => $colab::hostnames,
  }

  $package_defaults = {
    before => Pip::Install['pyOpenSSL'],
  }

  case $osfamily {

    'Redhat': {
      ensure_packages(['java-1.7.0-openjdk', 'fuse-sshfs'], $package_defaults)
    }
    'Debian': {
      ensure_packages(['openjdk-7-jre', 'sshfs'], $package_defaults)
    }
  }

  ensure_packages(['memcached'])

  # Punjab dep
  pip::install { 'Twisted': }
  pip::install { 'pyOpenSSL': }

  # XMPP connection manager
  pip::install { 'punjab':
    require => Pip::Install['Twisted', 'pyOpenSSL'],
  }

  supervisor::app { 'punjab':
    command   => 'twistd --nodaemon punjab',
    directory => '/home/colab/',
    user      => 'colab',
  }

  supervisor::app { 'solr':
    command   => 'java -jar start.jar',
    directory => $colab::solr_project_path,
    user      => 'colab',
  }

  supervisor::app { 'mailmanapi':
    command   => '/home/colab/.virtualenvs/colab/bin/mailman-api.py -b 127.0.0.1:9000',
    directory => '/home/colab/',
    user      => 'colab',
  }
}
