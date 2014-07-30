
class colab {

  require pip

  include appdeploy::deps::lxml
  include appdeploy::deps::postgresql
  include colab::cronjobs

  appdeploy::django { 'colab':
    user      => 'colab',
    directory => '/home/colab/colab/src',
    proxy_hosts => [
      'colab.interlegis.leg.br',
    ],

  }

  ensure_packages(['mercurial', 'openjdk-7-jre', 'memcached', 'sshfs'])

  # XMPP connection manager
  package { 'punjab':
    ensure   => installed,
    provider => pip,
  }

  # Punjab dep
  package { 'Twisted':
    ensure   => installed,
    provider => pip,
  }

  # Punjab dep
  package { 'pyOpenSSL':
    ensure   => installed,
    provider => pip,
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
}
