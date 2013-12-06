
class colab::requirements {

  # req for cloning code
  package { 'git':
    ensure => installed,
  }

  package { 'mercurial':
    ensure => installed,
  }

  # req to install python pkgs
  package { 'python-pip':
    ensure => installed,
  }

  # req to create virtualenvs
  package { 'virtualenvwrapper':
    ensure   => installed,
    provider => pip,
    require  => Package['python-pip'],
  }

  # XMPP connection manager
  package { 'punjab':
    ensure   => installed,
    provider => pip,
    require  => Package['python-pip'],
  }

  # Punjab dep
  package { 'Twisted':
    ensure   => installed,
    provider => pip,
    require  => Package['python-pip'],
  }

  # Punjab dep
  package { 'pyOpenSSL':
    ensure   => installed,
    provider => pip,
    require  => [Package['python-pip'], Package['python-dev'], Package['build-essential']],
  }

  # links virtualenvwrapper to load automaticaly
  file { '/etc/bash_completion.d/virtualenvwrapper.sh':
    ensure => link,
    target => '/usr/local/bin/virtualenvwrapper.sh',
  }

  # req for any compilation
  package { 'build-essential':
    ensure => installed,
  }

  # req for compiling every python pkg
  package { 'python-dev':
    ensure => installed,
  }

  # req by gvent
  package { 'libevent-dev':
    ensure => installed,
  }

  # req by psycopg2
  package { 'libpq-dev':
    ensure => installed,
  }

  # req by feedzilla
  package { 'libxml2-dev':
    ensure => installed,
  }

  # req by feedzilla
  package { 'libxslt1-dev':
    ensure => installed,
  }

  # req by Django L10N
  package { 'gettext':
    ensure => installed,
  }

  # req by solr
  package { 'openjdk-7-jre':
    ensure => installed,
  }

  package { 'memcached':
    ensure => installed,
  }

  package { 'libjpeg-dev':
    ensure => installed,
  }

  package { 'zlib1g-dev':
    ensure => installed,
  }

  package { 'libfreetype6-dev':
    ensure => installed,
  }

  package { 'sshfs':
    ensure => installed,
  }
}
