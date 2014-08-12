#!/bin/bash

# Pré-requisitos

# Atualizacao
sudo yum update -y

## Instalação do Trac 0.12

# 0. Adicionando o repositório EPEL
sudo yum install -y wget
sudo wget -O /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6 https://www.fedoraproject.org/static/0608B895.txt
sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6

# 0. Adicionando o repositório PUIAS
sudo rpm -Uvh https://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-puias

# 1. Libere a porta 5000 desta máquina para que máquina do colab possa ouvi-la
#sudo iptables -A INPUT -p tcp -dport 5000 -j ACCEPT
#sudo /sbin/service iptables save

# 2. Instale as dependências

sudo yum install gcc python-devel python-setuptools vim -y
sudo yum install postgresql-devel -y

# 3. Instale o pacote python para a utilização do postgres

sudo easy_install psycopg2

# 4. Instale o Trac

sudo yum install -y trac

# 5. Inicie o Trac

sudo mkdir -p /opt/trac
sudo trac-admin /opt/trac initenv colab postgres://colab:colab@/trac_colab?host=$1

## 6. Instale o subversion

sudo yum install subversion -y

## 7. Crie uma pasta para os repositório SVN
#
#sudo mkdir /opt/repos
#
## 8. Edite o arquivo de configuração do Trac
#
##sudo vim /opt/trac/conf/trac.ini
#
##Mude a linha
#
##    repository_dir =
#
## para
#
##    repository_dir = /opt/repos/
#
## Dentro da tag [trac] coloque
#
##    obey_remote_user_header = true
#
## Insira as linhas a seguir no final do arquivo
#
##    [components]
##    tracopt.versioncontrol.svn.* = enabled
#
##    [ESC]:wq!
#
#
## 9. Crie o plugin do remote user

sudo wget https://gitlab.com/softwarepublico/colabdocumentation/raw/master/Arquivos/remote-user-auth.py -O /opt/trac/plugins/remote-user-auth.py
sudo sed -i "s/\[trac\]/\[trac\]\nobey_remote_user_header = true/" /opt/trac/conf/trac.ini

## 10. Instale o supervisor

sudo yum install -y supervisor

## 11. Modifique o arquivo de configuração

sudo sh -c "echo \"[program:trac]
command=/usr/sbin/tracd --port 5000 /opt/trac
directory=/opt/trac
user=root
autostart=true
autorestart=false
redirect_stderr=True\" >> /etc/supervisord.conf"

## 12. Reinicie o supervisor

sudo service supervisord start
