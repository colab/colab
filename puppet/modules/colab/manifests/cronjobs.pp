
class colab::cronjobs {

  $virtualenv_python = "/home/colab/.virtualenvs/colab/bin/python"
  $manage_colab = "$virtualenv_python ~/colab/src/manage.py"

  Cron {
    user => colab,
  }

  cron { 'feedzilla':
    command => "$manage_colab feedzilla_update &> /dev/null",
    hour    => '*',
    minute  => '0',
  }

  cron { 'update-badges':
    command => "$manage_colab update_badges &> /dev/null",
    hour    => '*',
    minute  => '*/5',
  }

  cron { 'update-haystack-index':
    command => "$manage_colab update_index --age=1 &> /dev/null",
    hour    => '*',
    minute  => '*',
  }

  cron { 'rebuild-haystack-index':
    command => "$manage_colab rebuild_index --noinput &> /dev/null",
    hour    => '2',
    minute  => '34',
  }

  cron { 'import-mailman-messages':
    command => "$manage_colab import_emails --archives_path=/mnt/mailman/archives/ --exclude-list=saberes-divulgacao --exclude-list=pml --exclude-list=mailman --exclude-list=lexml-anuncios &> /dev/null",
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

  #cron { 'mount-sshfs':
  #  command => 'test -e /mnt/mailman/archives/flag || sshfs root@listas.interlegis.gov.br:/var/lib/mailman/archives/private /mnt/mailman/archives/ -o ro,nosuid,nodev,max_read=65536,allow_other,IdentityFile=/root/.ssh/id_rsa && touch /mnt/mailman/archives/flag &> /dev/null',
  #  minute  => '*/5',
  #  user    => 'root',
  #  require => [
  #      File['/mnt/mailman/archives/'],
  #      #File['root-ssh-private-key'],
  #      Package['sshfs'],
  #  ],
  #}

  cron { 'cleanup-snippets':
    command => "$manage_colab cleanup_snippets &> /dev/null",
    hour    => '1',
  }

}
