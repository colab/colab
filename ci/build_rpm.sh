#!/bin/bash

if [ "$TRAVIS_BRANCH" != "ci-package" ]; then
  exit 0;
fi

python setup.py sdist

sudo apt-get install rinse > /dev/null

sudo rinse --arch="amd64" --distribution="centos-7" --directory="/tmp/centos-7" --config="ci/rinse.conf" --pkgs-dir="ci/"

sudo mkdir -p /tmp/centos-7/root/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
sudo cp dist/colab-*.tar.gz /tmp/centos-7/root/rpmbuild/SOURCES/
sudo cp colab.spec /tmp/centos-7/root/rpmbuild/SPECS/
sudo cp ci/colab.repo /tmp/centos-7/etc/yum.repos.d/
sudo cp ci/softwarepublico.key /tmp/centos-7/etc/yum.repos.d/

# Commands on chroot

sudo chroot /tmp/centos-7/ yum install rpm-build -y > /dev/null
sudo chroot /tmp/centos-7/ yum install python-virtualenv colab-deps -y /dev/null
sudo HOME=/root chroot /tmp/centos-7/ rpmbuild -ba /root/rpmbuild/SPECS/colab.spec

# Send to packagecloud

gem install package_cloud
PACKAGE_PATH=`sudo find /tmp/centos-7/root/rpmbuild/RPMS/noarch/ -name "colab*.rpm"`
sudo package_cloud push seocam/colab-$TRAVIS_BRANCH/el/7 $PACKAGE_PATH
