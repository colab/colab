#!/bin/bash

python setup.py sdist

sudo apt-get install rinse

sudo rinse --arch="amd64" --distribution="centos-7" --directory="/tmp/centos-7" --config="ci/rinse.conf" --pkgs-dir="ci/"

sudo mkdir -p /tmp/centos-7/root/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
sudo cp dist/colab-*.tar.gz /tmp/centos-7/root/rpmbuild/SOURCES/
sudo cp colab.spec /tmp/centos-7/root/rpmbuild/SPECS/
sudo cp ci/colab.repo /tmp/centos-7/etc/yum.repos.d/
sudo cp ci/softwarepublico.key /tmp/centos-7/etc/yum.repos.d/

# Commands on chroot

set -e

sudo chroot /tmp/centos-7/ yum install rpm-build
sudo chroot /tmp/centos-7/ yum install python-virtualenv colab-deps
sudo HOME=/root chroot /tmp/centos-7/ rpmbuild -ba /root/rpmbuild/SPECS/colab.spec
