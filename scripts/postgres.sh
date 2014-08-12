#!/bin/bash

set -x

if [ ! "$1" ]
  then
      echo "Arquivo de configuracao nao encontrado."
      echo "./postgres.sh <CONFIG_FILE>"
      exit -1
fi

CONFIG_FILE=$1

sudo yum localinstall http://yum.postgresql.org/9.3/redhat/rhel-6-x86_64/pgdg-centos93-9.3-1.noarch.rpm -y
sudo yum install  postgresql-devel  postgresql93 postgresql93-devel postgresql93-libs postgresql93-server vim wget -y

sudo service postgresql-9.3 initdb

sudo chkconfig postgresql-9.3 on

sudo service postgresql-9.3 start

echo "export PATH=$PATH:/usr/pgsql-9.3/bin/" >> ~/.bashrc
source ~/.bashrc
sudo sh -c "echo 'export PATH=$PATH:/usr/pgsql-9.3/bin/' >> ~/.bashrc"
sudo sh -c "source /root/.bashrc"

sudo sed -i 's/\/sbin:\/bin:\/usr\/sbin:\/usr\/bin/\/sbin:\/bin:\/usr\/sbin:\/usr\/bin:\/usr\/pgsql-9.3\/bin/' /etc/sudoers

sudo -u postgres psql -c "CREATE USER colab SUPERUSER INHERIT CREATEDB CREATEROLE;"
sudo -u postgres psql -c "ALTER USER colab PASSWORD 'colab';"
sudo -u postgres psql -c "CREATE USER git SUPERUSER INHERIT CREATEDB CREATEROLE;"
sudo -u postgres psql -c "CREATE ROLE redmine LOGIN ENCRYPTED PASSWORD 'redmine' NOINHERIT VALID UNTIL 'infinity';"
sudo -u postgres psql -c "CREATE DATABASE colab WITH OWNER colab ENCODING 'UTF8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8' TEMPLATE=template0;"
sudo -u postgres psql -c "CREATE DATABASE trac_colab WITH OWNER colab ENCODING 'UTF8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8' TEMPLATE=template0;"
sudo -u postgres psql -c "CREATE DATABASE redmine WITH ENCODING='UTF8' OWNER=redmine;"

sudo wget https://gitlab.com/softwarepublico/colabdocumentation/raw/master/Arquivos/postgres/pg_hba.conf -O /var/lib/pgsql/9.3/data/pg_hba.conf

source $CONFIG_FILE

sudo sed -i "s/host    redmine                         redmine         127.0.0.1\/32            md5/host    redmine                         redmine         $REDMINE_IP\/32            md5/" /var/lib/pgsql/9.3/data/pg_hba.conf
sudo sed -i "s/host    trac_colab                      colab           127.0.0.1\/32            md5/host    trac_colab                      colab           $TRAC_IP\/32            md5/" /var/lib/pgsql/9.3/data/pg_hba.conf
sudo sed -i "s/host    colab                           colab           127.0.0.1\/32            md5/host    colab                           colab           $COLAB_IP\/32            md5/" /var/lib/pgsql/9.3/data/pg_hba.conf
sudo sed -i "s/host    gitlabhq_production             git             127.0.0.1\/32            trust/host    gitlabhq_production             git             $GITLAB_IP\/32            trust/" /var/lib/pgsql/9.3/data/pg_hba.conf

sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /var/lib/pgsql/9.3/data/postgresql.conf

sudo service postgresql-9.3 restart

