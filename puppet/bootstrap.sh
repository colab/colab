#!/bin/bash

PUPPET_VERSION=`dpkg -l | grep puppet-common | awk '{ print $3 }'`

if [ "$PUPPET_VERSION" != '3.2.3-1puppetlabs1' ] ; then 
    wget -O /tmp/puppet_apt.deb http://apt.puppetlabs.com/puppetlabs-release-precise.deb &> /dev/null
    dpkg -i /tmp/puppet_apt.deb
    DEBIAN_FRONTEND=noninteractive apt-get update -y
    DEBIAN_FRONTEND=noninteractive apt-get install puppet -y
fi

cp /vagrant/puppet/hiera.yaml /etc/puppet/hiera.yaml -f
