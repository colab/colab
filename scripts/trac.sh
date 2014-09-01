#!/bin/bash

if [[ ! "$1" ]]
        then
        echo " Parametro nao encontrado."
        echo " ./tra.sh <DATABASE_HOST>"
        exit -1
fi

DATABASE_HOST=$1

sudo rm -rf /opt/trac

if [[ $DATABASE_HOST == "127.0.0.1" ]]; then
	sudo -u postgres psql -c "DROP DATABASE trac_colab;"
	sudo -u postgres psql -c "CREATE DATABASE trac_colab WITH OWNER colab ENCODING 'UTF8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8' TEMPLATE=template0;"
fi

sudo yum install -y wget
sudo wget -O /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6 https://www.fedoraproject.org/static/0608B895.txt
sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6

sudo rpm -Uvh https://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-puias

sudo yum install gcc python-devel python-setuptools vim -y
sudo yum install postgresql-devel -y

sudo easy_install psycopg2

sudo yum install -y trac

sudo mkdir -p /opt/trac
sudo trac-admin /opt/trac initenv colab postgres://colab:colab@/trac_colab?host=$DATABASE_HOST

sudo yum install subversion -y

sudo wget https://gitlab.com/softwarepublico/colabdocumentation/raw/master/Arquivos/remote-user-auth.py -O /opt/trac/plugins/remote-user-auth.py
sudo sed -i "s/\[trac\]/\[trac\]\nobey_remote_user_header = true/" /opt/trac/conf/trac.ini

sudo yum install -y supervisor

sudo sh -c "echo \"[program:trac]
command=/usr/sbin/tracd --port 5000 /opt/trac
directory=/opt/trac
user=root
autostart=true
autorestart=false
redirect_stderr=True\" > /etc/supervisor/conf.d/trac.conf"

sudo service supervisord start

