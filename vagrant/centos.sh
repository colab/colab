#!/bin/bash

### Disable annoying plugin
sed -i'' s/enabled=1/enabled=0/g /etc/yum/pluginconf.d/fastestmirror.conf

### Add PUIAS repo

yum install curl -y

if [ ! -f /etc/pki/rpm-gpg/RPM-GPG-KEY-puias ]; then
    curl -s http://www.math.ias.edu/data/puias/6/i386/os/RPM-GPG-KEY-puias > /etc/pki/rpm-gpg/RPM-GPG-KEY-puias
fi

if [ ! -f /etc/yum.repos.d/puias-6-core.repo ]; then
    rpm -i --nodeps http://springdale.math.ias.edu/data/puias/6/x86_64/os/Packages/springdale-release-6-6.5.0.45.sdl6.3.x86_64.rpm --replacefiles

    rpm -i --nodeps http://springdale.math.ias.edu/data/puias/6/x86_64/os/Packages/springdale-core-6-2.sdl6.10.noarch.rpm
fi

if [ ! -f /etc/yum.repos.d/puias-6-computational.repo ]; then
    yum install springdale-computational -y
fi


### Install dependencies

yum -y groupinstall "Development tools"

yum install -y git unzip mercurial libev-devel gettext libxml2-devel libxslt-devel openssl-devel libffi-devel libjpeg-turbo-devel zlib-devel freetype-devel postgresql-devel python27 python27-devel postgresql-server

### Install Virtualenvwrapper
which pip2.7 > /dev/null ||
    curl -s -L https://raw.githubusercontent.com/pypa/pip/1.5.6/contrib/get-pip.py |
        python2.7

if [ ! -f /etc/profile.d/virtualenvwrapper.sh ]
then
    pip install virtualenvwrapper
    cat > "/etc/profile.d/virtualenvwrapper.sh" <<EOF
export VIRTUALENVWRAPPER_PYTHON="/usr/bin/python2.7"
source /usr/bin/virtualenvwrapper.sh
EOF
fi

### Create conf directory
mkdir -p /etc/colab
chown vagrant:vagrant /etc/colab


## Configuring postgres
if [ ! -f /var/lib/pgsql/data/pg_hba.conf.bkp ]; then
    cp /var/lib/pgsql/data/pg_hba.conf /var/lib/pgsql/data/pg_hba.conf.bkp
    echo "host  all  colab  127.0.0.1/32  md5" > /var/lib/pgsql/data/pg_hba.conf
    echo "host  all  colab  ::1/128       md5" >> /var/lib/pgsql/data/pg_hba.conf
    service postgresql initdb &> /dev/null
    service postgresql restart
fi


### Create colab user in PostgreSQL
echo "CREATE USER colab WITH PASSWORD 'colab';" | sudo -u postgres -i psql 2> /dev/null || echo

#i## Create colab DB in PostgreSQL
sudo -u postgres -i createdb --owner=colab colab 2> /dev/null | echo
