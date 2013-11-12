
class colab::cronjobs {

  $virtualenv_python = "/home/colab/.virtualenvs/colab/bin/python"
  $manage_colab = "$virtualenv_python colab/src/manage.py"

  Cron {
    user => colab,
  }

  cron { 'update-haystack-index':
    command => "$manage_colab update_index --age=1",
    minute  => '*',
  }

  cron { 'rebuild-haystack-index':
    command => "$manage_colab rebuild_index --noinput",
    hour    => '2',
    minute  => '34',
  }

  cron { 'import-mailman-messages':
    command => "$manage_colab import_emails --archives_path=/usr/local/django/colab/mnt/archives/ --exclude-list=saberes-divulgacao --exclude-list=pml --exclude-list=mailman --exclude-list=lexml-anuncios",
    hour    => '*',
    minute  => '*',
  }

  file { '/mnt/mailman/':
    ensure => directory,
  }

  file { '/mnt/mailman/archives/':
    ensure  => directory,
    require => File['/mnt/mailman/'],
  }

  cron { 'mount-sshfs':
    command => 'test -e /mnt/mailman/archives/flag || sshfs root@listas.interlegis.gov.br:/var/lib/mailman/archives/private /mnt/mailman/archives/ -o ro,nosuid,nodev,max_read=65536,allow_other,IdentityFile=/root/.ssh/id_rsa && touch /mnt/mailman/archives/flag',
    minute  => '*/5',
    user    => 'root',
    require => [
        File['/mnt/mailman/archives/'],
        File['root-ssh-private-key'],
        Package['sshfs'],
    ],
  }

}
