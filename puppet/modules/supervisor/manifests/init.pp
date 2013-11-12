class supervisor {

  package { "supervisor":
    ensure   => installed,
    provider => pip,
  }

  service { "supervisord":
    ensure    => running,
    enable    => true,
    require   => [Package['supervisor'],
                  File['/etc/init.d/supervisord']],
    stop      => '/etc/init.d/supervisord stop',
    start     => '/etc/init.d/supervisord start',
    restart   => '/etc/init.d/supervisord restart',
    subscribe => File['/etc/supervisord.conf'],
  }

  case $operatingsystem {
    debian: { $supervisord_conf = "puppet:///modules/supervisor/debian-isnok-initscript" }
    ubuntu: { $supervisord_conf = "puppet:///modules/supervisor/ubuntu-initscript" }
  }

  file { '/etc/init.d/supervisord':
    source  => $supervisord_conf,
    mode    => '0755',
  }

  file { '/etc/supervisor':
    ensure => directory,
  }

  file { '/etc/supervisord.conf':
    source  => 'puppet:///modules/supervisor/supervisord.conf',
    require => File['/etc/supervisor'],
  }

  file { '/etc/supervisor/conf.d/':
    ensure  => directory,
    recurse => true,
    purge   => true,
    notify  => Service['supervisord'],
    require => File['/etc/supervisor'],
  }
}
