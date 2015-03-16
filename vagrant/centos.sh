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

yum -y groupinstall "Development tools"

yum install -y git unzip mercurial libev-devel gettext libxml2-devel libxslt-devel openssl-devel libffi-devel libjpeg-turbo-devel zlib-devel freetype-devel postgresql-devel python-devel postgresql-server java

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
    service postgresql initdb
    cp /var/lib/pgsql/data/pg_hba.conf /var/lib/pgsql/data/pg_hba.conf.bkp
    echo "local all  all                ident" > /var/lib/pgsql/data/pg_hba.conf
    echo "host  all  all  127.0.0.1/32  md5" >> /var/lib/pgsql/data/pg_hba.conf
    echo "host  all  all  ::1/128       md5" >> /var/lib/pgsql/data/pg_hba.conf
    service postgresql restart
fi


### Create colab user in PostgreSQL
echo "CREATE USER colab WITH PASSWORD 'colab';" | sudo -u postgres -i psql 2> /dev/null || echo
echo "ALTER USER colab CREATEDB;" | sudo -u postgres -i psql 2> /dev/null

### Create colab DB in PostgreSQL
sudo -u postgres -i createdb --owner=colab colab 2> /dev/null | echo

### Forcing postgresql to start at boot
sudo chkconfig postgresql on
