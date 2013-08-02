Puppet Supervisor
=================

Install and manage apps in supervisord


Usage
=================

Include supervisor class
```puppet
include supervisor
```

Install your app using defined type supervisor::app

```puppet
supervisor::app { 'your-app-title':
  app_name  => 'your-app-name' # Default to 'your-app-title'
  command   => 'The command that will be run this app', # required
  directory => 'Path where your command will be run' # required
  user      => 'User to execute this app' # Default to ubuntu
}
```