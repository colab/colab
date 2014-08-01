class colab::cronjobs {

  include colab::cronmailman

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

  cron { 'cleanup-snippets':
    command => "$manage_colab cleanup_snippets &> /dev/null",
    hour    => '1',
  }
}
