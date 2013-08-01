
class colab {
  # Common
  include ps1
  include vim
  include ntp
  include locale
  include timezone
  include postfix

  include supervisor
  include colab::requirements

  user { 'colab':
    ensure     => present,
    managehome => true,
    shell      => '/bin/bash',
  }

  mailalias { 'colab':
    ensure    => present,
    recipient => 'root',
  }
}
