#!/bin/sh

set -e

if [ -d /vagrant/colab ]; then
  basedir=/vagrant/colab
else
  basedir=/vagrant
fi

# very simple OS detection
if [ -x /usr/bin/apt-get ]; then
  exec sh $basedir/vagrant/ubuntu.sh
fi
if [ -x /usr/bin/yum ]; then
  exec sh $basedir/vagrant/centos.sh
fi
