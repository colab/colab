#!/bin/sh
#Instalação do Colab
#-------------------
#
#Siga os passo na máquina destinada ao Colab

IP_HOSTS=$1
COLAB_IP=$2
COLAB_PORT=$3

if [[ ! "$IP_HOSTS" || ! "$COLAB_IP" || ! "$COLAB_PORT"  ]]
        then
        echo " Parametros nao encontrados. Utiliza o caminho absoluto para o arquivo."
	echo ""
        echo " ./colab.sh <PATH_TO_IP_HOSTS.YML> <IP_COLAB_EXTERN> <PORT> "
 	echo ""
        echo "Utilize o modelo de ips: 
  wget https://gitlab.com/softwarepublico/colabdocumentation/raw/master/Arquivos/colab/ipconfig.yml -O /tmp/ipconfig.yml

Exemplo: ./colab.sh /tmp/ipconfig.yml 127.0.0.1 8000
"
        exit -1
fi


#
#*NOTE:*
#
#    Libere um acesso externo para esta máquina, pois o site do colab será acessado por esta máquina.
#
#Instale as ferramentas de desenvolvimento do python e algumas dependências para compilar o python
#
#.. code-block::
#
    sudo yum groupinstall "Development tools" -y
    sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel libxslt-devel vim -y
#
#Faça o download e compile o Python 2.7
#
#.. code-block::
#
    cd /tmp
    sudo wget --no-check-certificate https://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz
    sudo tar xf Python-2.7.6.tar.xz
    cd Python-2.7.6
    sudo ./configure --prefix=/usr/local
    sudo make
#
#Instale o python 2.7 como um python alternativo
#
#.. code-block::
#
    sudo make altinstall
#
#Atualize a variável PATH para executar o python2.7
#
#.. code-block::
#
    sudo sh -c "echo 'export PATH=$PATH:/usr/local/bin/' >> ~/.bashrc"
    sudo sh -c "source ~/.bashrc"
#
#Instale o easy_install para o python 2.7
#
#.. code-block::
#
    cd /tmp
    sudo wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
    sudo /usr/local/bin/python2.7 ez_setup.py
#
#Instale o pip 2.7
#
#.. code-block::
#
    sudo /usr/local/bin/easy_install-2.7 pip
#
#Instale alguns pacotes adicionais do python
#
#.. code-block::
#
    sudo yum remove libevent -y
    sudo yum install mercurial libevent-devel python-devel -y
#
#Edite o arquivo sudores para executar o ``python2.7`` como sudo
#
#
#Mude a linha
#
#
    sudo sed -i 's/\/sbin:\/bin:\/usr\/sbin:\/usr\/bin/\/sbin:\/bin:\/usr\/sbin:\/usr\/bin:\/usr\/local\/bin/' /etc/sudoers
#
#Instalando o Django 1.6
#
#Instale o django e o uwsgi
#
#.. code-block::
#
    sudo pip2.7 install django
    sudo pip2.7 install uwsgi
#
#Instale o Colab
#
#Instale o git e clone o repositório do colab
#
#.. code-block::

   #Verifica se git instalado para não conflitar com gitlab
   git_loc=`type -p $1`
   if [[ ! "$git_loc" ]]  
   then
     sudo yum install git -y
   fi

    cd /opt
    sudo git clone https://github.com/colab-community/colab.git -b dev_spb
#
#Instale os pré-requisitos do colab
#
#.. code-block::
#
    sudo yum install postgresql-devel -y #Foi preciso adicionar esta linha quando o postgrsql não é instalado na mesma máquina
    sudo pip2.7 install mimeparse
    sudo pip2.7 install -r /opt/colab/requirements.txt
#
#Crie o arquivo local_settings na pasta src/colab
#
#.. code-block::
#
    sudo cp /opt/colab/src/colab/local_settings-dev.py /opt/colab/src/colab/local_settings.py
#
#Edite o arquivo local_settings criado, nele deverão ser alterados os IPs das máquinas utilizadas
#
#.. code-block::
#    
     TRAC_IP=`sed -n 1p $1 | grep -Po "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"`
     GITLAB_IP=`sed -n 2p $1 | grep -Po "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"`
     REDMINE_IP=`sed -n 3p $1 | grep -Po "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"`


#Troque os IPs das seguintes linhas
#
#.. code-block::
#
    sudo sed -i "s/http:\/\/localhost:5000\/trac\//http:\/\/$TRAC_IP:5000\/trac\//g" /opt/colab/src/colab/local_settings.py
    sudo sed -i "s/http:\/\/localhost:8090\/gitlab\//http:\/\/$GITLAB_IP:8090\/gitlab\//g" /opt/colab/src/colab/local_settings.py
    sudo sed -i "s/http:\/\/localhost:9080\/redmine\//http:\/\/$REDMINE_IP:9080\/redmine\//g" /opt/colab/src/colab/local_settings.py

#Na máquina do colab, sincronize e migre o banco de dados.
#
#.. code-block::
#
#Passo adicionado: Recebendo o IP onde está instalado o Postgresql

    DATABASE_IP=`sed -n 4p $1 | grep -Po "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"`

    sudo sed -i "s/DATABASES\['default'\]\['HOST'\] = '[^']\+'/DATABASES\['default'\]\['HOST'\] = '$DATABASE_IP'/g" /opt/colab/src/colab/local_settings.py
    sudo sed -i "s/DATABASES\['trac'\]\['HOST'\] = '[^']\+'/DATABASES\['trac'\]\['HOST'\] = '$DATABASE_IP'/g" /opt/colab/src/colab/local_settings.py

    cd /opt/colab/src
    python2.7 manage.py syncdb
    python2.7 manage.py migrate

#Atualize o index com o solr, para executar esta ação o solr já deve estar funcionando na máquina voltada para o Solr
#
#.. code-block::
#
	SOLR_IP=`sed -n 5p $1 | grep -Po "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"`
	sudo sed -i "s/HAYSTACK_CONNECTIONS\['default'\]\['URL'\] = '[^']\+'/HAYSTACK_CONNECTIONS\['default'\]\['URL'\] = 'http:\/\/$SOLR_IP:8983\/solr\/'/g" /opt/colab/src/colab/local_settings.py

        cd /opt/colab/src
        python2.7 manage.py update_index

#Importe os e-mails do mailman
#
#.. code-block::
#
    sudo python2.7 /opt/colab/src/manage.py import_emails
#
#Crie os Cronjobs para rodar em background a importação de email e a atualização do index
#
#.. code-block::
#
  sudo sh -c "echo \"5 * * * * /usr/bin/python2.7 /opt/colab/src/manage.py import_emails
45 * * * * /usr/bin/python2.7 /opt/colab/src/manage.py update_index\" > /tmp/crontabs"
  sudo crontab /tmp/crontabs

#Instale a inicialização do colab como serviço
# Adicionando o repositório PUIAS(para o supervisor)
sudo rpm -Uvh https://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-puias

sudo yum install supervisor -y

sudo sh -c "echo \"[program:colab]
command=/usr/local/bin/python2.7 /opt/colab/src/manage.py runserver $2:$3
directory=/opt/colab
user=colab
autostart=true
autorestart=false
redirect_stderr=true\" >> /etc/supervisord.conf"


## 12. Reinicie o supervisor

sudo service supervisord restart
