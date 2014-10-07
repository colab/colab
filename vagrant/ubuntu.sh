#!/bin/bash

UBUNTU=$(lsb_release -sc)

if [[ $UBUNTU == 'precise' ]]
then
    postgresql_pkg='postgresql-9.1'
elif [[ $UBUNTU == 'trusty' ]]
then
    postgresql_pkg='postgresql-9.3'
fi


### Install dependencies
apt-get update

apt-get install curl git unzip mercurial build-essential libev-dev gettext libxml2-dev libxslt1-dev libssl-dev libffi-dev libjpeg-dev zlib1g-dev libfreetype6-dev libpq-dev python-dev $postgresql_pkg -y


### Install Virtualenvwrapper
which pip2.7 > /dev/null ||
    curl -s -L https://raw.githubusercontent.com/pypa/pip/1.5.6/contrib/get-pip.py |
        python2.7

if [ ! -L /etc/bash_completion.d/virtualenvwrapper.sh ]
then
    pip install virtualenvwrapper
    ln -s /usr/local/bin/virtualenvwrapper.sh /etc/bash_completion.d/virtualenvwrapper.sh
fi

### Create conf directory
mkdir -p /etc/colab
chown vagrant:vagrant /etc/colab

### Create colab user in PostgreSQL
echo "CREATE USER colab WITH PASSWORD 'colab';" | sudo -u postgres -i psql 2> /dev/null || echo

#i## Create colab DB in PostgreSQL
sudo -u postgres -i createdb --owner=colab colab 2> /dev/null | echo
