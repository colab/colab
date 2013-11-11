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
  app_name     => 'your-app-name' # Default to 'your-app-title'
  command      => 'The command that will be run this app', # required
  directory    => 'Path where your command will be run' # required
  user         => 'User to execute this app' # Default to ubuntu
  startsecs    => 'The total number of seconds which the program needs to stay running after a startup to consider the start successful' # Default to undef
  stopwaitsecs => 'The number of seconds to wait for the OS to return a SIGCHILD to supervisord after the program has been sent a stopsignal', # Default to undef
  priority     => 'The relative priority of the program in the start and shutdown ordering' # Default to undef
}
```
