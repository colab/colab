#!/bin/sh

set -e

for dir in /vagrant/colab /vagrant; do
    if [ -f $dir/setup.py ]; then
        basedir="$dir"
        break
    fi
done

# very simple OS detection
if [ -x /usr/bin/apt-get ]; then
  exec $basedir/vagrant/ubuntu.sh
fi
if [ -x /usr/bin/yum ]; then
  exec $basedir/vagrant/centos.sh
fi
