# Class: nginx
#
# Install nginx.
#
# Parameters:
# * $user. Defaults to 'www-data'.
# * $worker_processes. Defaults to '1'.
# * $worker_connections. Defaults to '1024'.
# * $error_log. Default to undef
# * $pid_file. Default to undef
# * $access_log. Default to undef
#
# Create config directories :
# * /etc/nginx/conf.d for http config snippet
# * /etc/nginx/includes for sites includes
#
# Provide 3 definitions :
# * nginx::config (http config snippet)
# * nginx::site (http site)
# * nginx::site_include (site includes)
#
# Templates:
#   - nginx.conf.erb => /etc/nginx/nginx.conf
#
class nginx (
  $user = 'www-data',
  $worker_processes = '1',
  $worker_connections = '1024',
  $error_log = undef,
  $pid_file = undef,
  $access_log = undef
){
  $nginx_includes = '/etc/nginx/includes'
  $nginx_conf = '/etc/nginx/conf.d'

  case $::operatingsystem {
    centos,fedora,rhel: {
      $nginx_packages = ['nginx', 'GeoIP', 'gd', 'libXpm', 'libxslt']
    }
    debian,ubuntu: {
      $nginx_packages = 'nginx-extras'
    }
  }
  if ! defined(Package[$nginx_packages]) { 
    package { $nginx_packages: 
      ensure => latest
    }
  }

  #restart-command is a quick-fix here, until http://projects.puppetlabs.com/issues/1014 is solved
  service { 'nginx':
    ensure     => running,
    enable     => true,
    hasrestart => true,
    require    => File['/etc/nginx/nginx.conf'],
    restart    => '/etc/init.d/nginx reload'
  }

  file { '/etc/nginx/nginx.conf':
    ensure  => present,
    mode    => '0644',
    owner   => 'root',
    group   => 'root',
    content => template('nginx/nginx.conf.erb'),
    notify  => Service['nginx'],
    require => Package[$nginx_packages],
  }

  file { $nginx_conf:
    ensure  => directory,
    mode    => '0644',
    owner   => 'root',
    group   => 'root',
    require => Package[$nginx_packages],
  }

  file { '/etc/nginx/ssl':
    ensure  => directory,
    mode    => '0644',
    owner   => 'root',
    group   => 'root',
    require => Package[$nginx_packages],
  }

  file { $nginx_includes:
    ensure  => directory,
    mode    => '0644',
    owner   => 'root',
    group   => 'root',
    require => Package[$nginx_packages],
  }

  # Nuke default files
  file { '/etc/nginx/fastcgi_params':
    ensure  => absent,
    require => Package[$nginx_packages],
  }

  file { '/etc/nginx/sites-enabled/default':
    ensure => absent,
  }
}
