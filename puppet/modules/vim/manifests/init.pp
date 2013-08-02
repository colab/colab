class vim (
  $vim_file = 'puppet:///modules/vim/vimrc.local'
  ) {

  if ! defined(Package['vim']) {
    package { 'vim':
      ensure => installed
    }
  }

  file { 'editor_vim':
    path    => '/etc/profile.d/editor.sh',
    ensure  => present,
    content => 'export EDITOR="vim"',
  }

  file { 'vimrc':
    path   =>   '/etc/vim/vimrc.local',
    ensure => present,
    source => $vim_file
  }

}
