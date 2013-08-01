Puppet ntp
==========
Start a cronjob to run every hour ntpdate

Usage
==========

```puppet
include ntp # Use default server (pool.ntp.org) or your hiera config (puppet 3+)
```
or
```puppet
class { 'ntp':
  server => 'your ntp server'
}
```