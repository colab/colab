
class postfix (
  $admin_email,
  $server_name=$fqdn,
  $mailbox_limit=0 # Zero means no limit
) {

  $postfix_preseed = '/var/cache/debconf/postfix.preseed'
  $preseed_cmd = "debconf-set-selections $postfix_preseed"

  file { $postfix_preseed:
    ensure  => present,
    content => template('postfix/postfix.preseed.erb'),
  }

  exec { $preseed_cmd:
    path        => '/usr/bin/',
    refreshonly => true,
    subscribe   => File[$postfix_preseed],
  }

  package { 'postfix':
    ensure       => installed,
    require      => File[$postfix_preseed],
    responsefile => $postfix_preseed,
  }

  package { 'mailutils':
    ensure => installed,
  }

  service {'postfix':
    ensure    => running,
    enable    => true,
    hasstatus => false,
    stop      => 'invoke-rc.d postfix stop',
    start     => 'invoke-rc.d postfix start',
    restart   => 'invoke-rc.d postfix restart',
    require   => Package['postfix']
  }
}
