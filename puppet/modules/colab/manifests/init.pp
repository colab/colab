
class colab {
  # Common
  include ps1
  include vim
  include ntp
  include locale
  include timezone
  include postfix

  include nginx
  include supervisor
  include colab::requirements

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

  supervisor::app { 'colab':
    command   => '/home/colab/.virtualenvs/colab/bin/gunicorn colab.wsgi:application -t 300',
    directory => '/home/colab/colab/src/',
    user      => 'colab',
  }

  supervisor::app { 'punjab':
    command   => 'twistd --nodaemon punjab',
    directory => '/home/colab/',
    user      => 'colab',
  }

  nginx::config { 'nginx':
    content => template('colab/nginx/extra_conf.erb'),
  }

  nginx::site { '000-colab':
    content => template('colab/nginx/site_default.erb'),
  }
}
