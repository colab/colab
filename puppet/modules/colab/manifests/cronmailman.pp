class colab::cronmailman {
  file { '/etc/cron.d/import_mailman_messages':
    content => template('colab/import_mailman_messages.erb'),
    ensure  => present,
  }
}
