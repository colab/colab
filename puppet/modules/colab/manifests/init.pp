
class colab {
  # Common
  include apt
  include ps1
  include vim
  include ntp
  include locale
  include timezone
  include postfix

  include supervisor
  include colab::requirements
  include colab::cronjobs

  apt::ppa { 'ppa:nginx/stable': }

  class { 'nginx':
    require => Apt::Ppa['ppa:nginx/stable'],
  }

  Mailalias {
    notify  => Exec['newaliases'],
    require => Class['postfix'],
  }

  exec { 'newaliases':
    command     => 'sendmail -bi',
    path        => '/usr/sbin',
    refreshonly => true,
  }

  group { 'colab':
    ensure => present,
  }

  user { 'colab':
    ensure     => present,
    managehome => true,
    shell      => '/bin/bash',
    gid        => 'colab',
    groups     => ['sudo'],
  }

  mailalias { 'colab':
    ensure    => present,
    recipient => 'root',
  }

  file { 'colab-sudoers':
    ensure  => present,
    path    => '/etc/sudoers.d/colab-sudoers',
    source  => 'puppet:///modules/colab/colab-sudoers',
    mode    => '0440',
    owner   => root,
    group   => root,
  }

  file { 'root-ssh-dir':
    ensure => directory,
    mode   => '0700',
    path   => '/root/.ssh',
  }

  # Should generate instead of copying
  #file { 'root-ssh-private-key':
  #  ensure  => present,
  #  mode    => '0600',
  #  path    => '/root/.ssh/id_rsa',
  #  source  => 'puppet:///modules/colab/root_id_rsa',
  #  owner   => root,
  #  group   => root,
  #}

  #file { 'root-ssh-public-key':
  #  ensure  => present,
  #  mode    => '0644',
  #  path    => '/root/.ssh/id_rsa.pub',
  #  source  => 'puppet:///modules/colab/root_id_rsa.pub',
  #  owner   => root,
  #  group   => root,
  #}

  supervisor::app { 'colab':
    command   => '/home/colab/.virtualenvs/colab/bin/gunicorn colab.wsgi:application -c colab/gunicorn.conf.py',
    directory => '/home/colab/colab/src/',
    user      => 'colab',
  }

  supervisor::app { 'punjab':
    command   => 'twistd --nodaemon punjab',
    directory => '/home/colab/',
    user      => 'colab',
  }

  supervisor::app { 'solr':
    command   => 'java -jar start.jar',
    directory => '/home/colab/apache-solr-3.6.2/example',
    user      => 'colab',
  }

  nginx::config { 'nginx':
    content => template('colab/nginx/extra_conf.erb'),
  }

  nginx::site { '000-colab':
    content => template('colab/nginx/site_default.erb'),
  }
}
