#!/bin/bash

set -ex

### Install dependencies
apt-get update

apt-get install curl git unzip mercurial build-essential libev-dev gettext libxml2-dev libxslt1-dev libssl-dev libffi-dev libjpeg-dev zlib1g-dev libfreetype6-dev libpq-dev python-dev postgresql virtualenvwrapper python-pip java-common -y


### Create conf directory
mkdir -p /etc/colab
chown vagrant:vagrant /etc/colab

### Create colab user in PostgreSQL
echo "CREATE USER colab WITH PASSWORD 'colab';" | sudo -u postgres -i psql 2> /dev/null || echo
echo "ALTER USER colab CREATEDB;" | sudo -u postgres -i psql 2> /dev/null

#i## Create colab DB in PostgreSQL
sudo -u postgres -i createdb --owner=colab colab 2> /dev/null | echo
