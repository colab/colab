
class colab::requirements {

  # req for cloning code
  package { 'git':
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
}