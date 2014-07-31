
class colab {

  require pip
  require appdeploy::deps::python
  require appdeploy::deps::essential

  include security_updates
  include appdeploy::deps::lxml
  include appdeploy::deps::postgresql
  include colab::cronjobs

  appdeploy::django { 'colab':
    user      => 'colab',
    directory => '/home/colab/colab/src',
    proxy_hosts => $colab::hostnames,
  }

  case $osfamily {
    'Redhat': {
      ensure_packages(['java-1.7.0-openjdk','fuse-sshfs'])
    }
    'Debian': {
      ensure_packages(['openjdk-7-jre','sshfs']) 
    }
  }

  ensure_packages(['memcached'])

  # XMPP connection manager
  pip::install { 'punjab': }

  # Punjab dep
  pip::install { 'Twisted': }
  pip::install { 'pyOpenSSL': }

  supervisor::app { 'punjab':
    command   => 'twistd --nodaemon punjab',
    directory => '/home/colab/',
    user      => 'colab',
  }

  supervisor::app { 'solr':
    command   => 'java -jar start.jar',
    directory => $colab::solr_project_path,
    user      => 'colab',
  }
}
