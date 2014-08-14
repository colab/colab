#!/bin/bash

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
sudo trac-admin /opt/trac initenv colab postgres://colab:colab@/trac_colab?host=$1

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
redirect_stderr=True\" >> /etc/supervisord.conf"

sudo service supervisord start

