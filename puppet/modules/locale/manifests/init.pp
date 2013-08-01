class locale (
  $locales  = 'en_US.UTF-8 pt_BR',
  $lang     = 'en_US.UTF-8',
  $language = 'en_US'
) {

  Exec {
    path => ['/usr/bin', '/usr/sbin', '/bin']
  }

  file { '/var/cache/locale':
    ensure => directory,
    mode   => '0755',
    owner  => 'root',
  }

  file { '/var/cache/locale/installed':
    ensure  => present,
    mode    => '0644',
    owner   => 'root',
    content => "${locales}-${lang}-${language}",
    require => File['/var/cache/locale'],
  }

  exec { 'install_locales':
    command => "locale-gen ${locales}",
    refreshonly => true,
    subscribe   => File['/var/cache/locale/installed'],
    notify  => Exec['reload_locales']
  }

  if $lang {
    exec { 'update_default_lang':
      command => "update-locale LANG='${lang}'",
      notify  => Exec['reload_locales'],
      refreshonly => true,
      subscribe   => File['/var/cache/locale/installed'],
    }
  }

  if $language {
    exec { 'update_default_language':
      command => "update-locale LANGUAGE='${language}'",
      notify  => Exec['reload_locales'],
      refreshonly => true,
      subscribe   => File['/var/cache/locale/installed'],
    }
  }

  exec { 'reload_locales':
    command     => "dpkg-reconfigure locales",
    refreshonly => true
  }

}

