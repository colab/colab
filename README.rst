.. -*- coding: utf-8 -*-

.. highlight:: rest

.. _colab_software:

=================================
Colab, a Software for Communities
=================================

What is Colab?
==============

Application that integrates existing systems to represent the contributions of the members through:

* The amendments to the Wiki trac system.

* Changes to the trac system code.

* Discussions at the mailman list.

* And other systems in the community.

Features
========

* Developerd by Interlegis Communities http://colab.interlegis.leg.br/

* Writed with Python http://python.org/

* Build in Django Web Framework https://www.djangoproject.com/

* Search engine with Solr https://lucene.apache.org/solr/

Colab and Solr
==============

This software uses Apache Solr as search platform based on Apache Lucene.

With Solr generates the REST style API with which you can make HTTP requests 
to get results: natively in XML or JSON, PHP, Ruby and Python and then treatment.

Installation
============

Installation instructions for Ubuntu 10.04
-------------------------------------------

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
