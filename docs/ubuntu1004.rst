.. -*- coding: utf-8 -*-

.. highlight:: rest

.. _ubuntu1004_install:

Installation instructions for Ubuntu 10.04
==========================================

.. contents :: :local:

Install Solr and dependencies
-----------------------------

* Install Java, tomcat, JDBC Postgres drivers (Ubuntu partner repositories must be enabled): ::

    sudo apt-get install sun-java6-bin tomcat6 libpg-java

* Download Solr 3.3 and extract it: ::

    wget http://archive.apache.org/dist/lucene/solr/3.3.0/apache-solr-3.3.0.tgz
    tar xzf apache-solr-3.3.0.tgz 

* Create the directory ``/var/local/lib/solr/`` and give the right permissions: ::

    sudo mkdir -p /var/local/lib/solr/
    sudo chown tomcat6:tomcat6 /var/local/lib/solr/

* Copy the solr home example to ``/usr/local/share/``: ::

    sudo cp -R apache-solr-3.3.0/example/solr /usr/local/share/

* Create a folder for libs in the solr home: ::

    sudo mkdir /usr/local/share/solr/lib/

* Copy Solr libs to libs folder: ::

    sudo cp apache-solr-3.3.0/dist/*.jar /usr/local/share/solr/lib/

* Copy Solr distribution to solr home: ::

    sudo cp apache-solr-3.3.0/dist/apache-solr-3.3.0.war /usr/local/share/solr/

* Link the JDBC Postgres drivers into the Solr installation: ::

    sudo ln -s /usr/share/java/postgresql-jdbc3-8.4.jar /usr/local/share/solr/lib/

* Link configurations to ``/etc`` ::

    sudo ln -s /usr/local/share/solr/conf/ /etc/solr

* Copy the configuration files from this folder into ``/etc/solr/``

* Link the ``solr-tomcat.xml`` file in the Tomcat configuration: ::

    sudo ln -s /etc/solr/solr-tomcat.xml /etc/tomcat6/Catalina/localhost/solr.xml 

* Check ``data-config.xml`` to make sure all information to connect to the databases are right

* Create a ``dataimport.properties`` on ``/etc/solr`` and give write access to ``tomcat6``: ::

    sudo touch /etc/solr/dataimport.properties
    sudo chown tomcat6:tomcat6 /etc/solr/dataimport.properties
 
* Restart tomcat: ::

    sudo /etc/init.d/tomcat6 restart

Install Colab and dependencies
------------------------------

* Install Apache2 with WSGI support: ::

    sudo apt-get install apache2 libapache2-mod-wsgi

* Install dependencies to compile psycopg2: ::

    sudo apt-get build-dep python-psycopg2

* Install Python PIP and update it: ::

    sudo apt-get install python-pip
    sudo pip install -U pip

* Install python virtualenv: ::

    sudo pip install virtualenv 

* Create a virtualenv for the deploy ::
 
    sudo mkdir /usr/local/django/
    sudo virtualenv /usr/local/django/colab/

* Download the colab ``src`` code: ::

    sudo hg clone https://bitbucket.org/seocam/atu-colab /usr/local/src/colab/

* Install the django site: ::

    sudo pip install /usr/local/src/colab -E /usr/local/django/colab/

* Configure your database settings in ``/usr/local/django/colab/lib/python2.6/site-packages/settings_local.py``
  
* Enable the colab site on apache and reload it: ::

    sudo ln -s /usr/local/django/colab/apache-site/colab /etc/apache2/sites-available
    sudo a2ensite colab
    sudo service apache2 restart

Configuring server to send emails
----------------------------------

* Install postfix and mailutils: ::

    sudo apt-get install mailutils postfix

* Update the file ``/etc/aliases`` adding users that should receive root's messages and run the update command: ::

    sudo newaliases


Cron job to import emails
---------------------------

* Install sshfs: ::

    sudo apt-get install sshfs autofs

* Create SSH keys. You should use a password but this tutorial won't cover it (if you use you will need to install and configure keychain process to be able to proceed): ::

    sudo ssh-keygen

* Copy the content of your key (``/root/.ssh/id_rsa.pub``) to the file ``/root/.ssh/authorized_keys`` on the mailinglist server.

* Append the following content to /etc/auto.master file: ::

    sudo /usr/local/django/colab/mnt /usr/local/django/colab/autofs/listas --timeout=600,--ghost

* Restart autofs: ::

    service autofs restart
  
* Link cron script into ``/etc/cron.d/`` folder: ::

    ln -s /usr/local/django/colab/etc/cron.d/colab_import_emails /etc/cron.d/ 
  
* From now on the emails should be imported every minute


Cron job to reindex Solr
-------------------------

* Install wget: ::

    sudo apt-get install wget

* Link cron script into ``/etc/cron.d/`` folder: ::

    sudo ln -s /usr/local/django/colab/etc/cron.d/colab_solr_reindex /etc/cron.d/

* From now on delta reindex should run every 10 minutes and full reindex once a day. 


Updating an installed version
------------------------------

* Update the source code: ::

    sudo cd /usr/local/src/colab/
    sudo hg pull
    sudo hg up
    sudo pip install /usr/local/src/colab/ -E /usr/local/django/colab/ -U
    sudo service apache2 restart
