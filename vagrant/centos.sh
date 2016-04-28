#!/bin/bash

set -ex

### Disable annoying plugin
sed -i'' s/enabled=1/enabled=0/g /etc/yum/pluginconf.d/fastestmirror.conf


if [ -n "$http_proxy" ]; then
    # force all repositories to always use the same host to take advantage of a
    # local proxy
    repos=$(grep -rl '^#baseurl' /etc/yum.repos.d)
    if [ -n "$repos" ]; then
        sed -i -e 's/^#baseurl/baseurl/; s/^mirrorlist=/#mirrorlist-/' $repos
    fi
fi


### Install dependencies

yum install -y epel-release

yum -y groupinstall "Development tools"

yum install -y git unzip gettext libxml2-devel libxslt-devel openssl-devel libffi-devel python-devel python-pip python-virtualenvwrapper redis

### Acceptance Tests dependencies

yum install -y Xvfb firefox

### Init Redis
systemctl enable redis
systemctl start redis
