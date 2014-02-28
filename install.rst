.. -*- coding: utf-8 -*-

.. highlight:: rest

.. _colab_software:

=================================
Installing a full colab environment
=================================

This file will guide you through the installation of colab's dependencys,
external tools and its integration with colab to help you start using/working.

The dependecys installation steps will be based of Ubuntu 13.04 but the tools,
integrations and the colab itself runs in a virtual machine so it'll be the same regardless of your system.


Fabric + VirtualBox + Vagrant
==============

You can easily install fabric using pip with

.. code-block::

  sudo apt-get install python-pip
  sudo pip install fabric

You can also instal Virtual Box with apt-get

.. code-block::

  sudo apt-get install virtualbox

Now, vagrant has an apt-get but its not supported anymore, so you'll have to manually download and install it from the site

  https://www.vagrantup.com/downloads.html

Starting the VM and environment
===============================

Clone the repository to your system

.. code-block::

  git clone https://github.com/colab-community/colab.git
  cd colab

Create your local configuration file(we'll adjust it later)

.. code-block::

  cp src/colab/local_settings-dev.py src/colab/local_settings.py

To startup the VM simple do

.. code-block::

  vagrant up

*NOTE*

  In case you have problems creating the virtual machine you might need to download the linux header files

  .. code-block::

    linux-headers-generic

Accessing the VM and configurating the database
===============================================

You should now be able to access your VM through

.. code-block::

  vagrant ssh

*NOTE*

  In case you get a connection port refused or ssh error, you might need to activate manually an ssh server(rare)

  .. code-block::

    sudo apt-get install ssh; sudo service ssh start;

The VM doesnt come with a databse so, you'll need to install one inside it.
Inside de VM download and install postgresql

.. code-block::

  sudo apt-get install postgresql

Access the postgresql database and create a new database and user colab user

.. code-block::

  sudo -u postgres psql
    CREATE USER colab SUPERUSER INHERIT CREATEDB CREATEROLE;
    ALTER USER colab PASSWORD 'colab';
    CREATE DATABASE colab;

Also, create the Trac's database(note it needs to support UTF8)

.. code-block::

  create database "trac_colab" with owner "colab" encoding 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8' TEMPLATE=template0;
  \q

That's the database used for Trac, but its needed so colab can make its migrations correctly and adjust solr accordinly

Installing Trac on the VM
=========================

Inside the VM(vagrant ssh) download e install trac

.. code-block::

  sudo apt-get install trac
  sudo pip install --upgrade Trac

Now you'll need to configure trac so it can access the previously created database. 

.. code-block::

  mkdir -p /var/local/trac
  sudo trac-admin /var/local/trac initenv

Set the project name to 'Colab' when asked, and the following postgresql connection string

.. code-block::

  postgres://colab:colab@/trac_colab?host=localhost

The trac database should be populated with relations, now need to give trac write access to its folders

.. code-block::

  sudo chown -R www-data /var/local/trac
  sudo chmod -R 775 /var/local/trac

Finally, trac can be run by

.. code-block::

  tracd --port 5000 /var/local/trac

Use port 8000 and access it on port 8080 in your local machine to see it works if you'd like(vagrant has port redirects)

Setting up Colab
=========================

You can exit the vagrant VM ('exit' inside the ssh shell) but for now leave it running Trac and start a new terminal tab

Open the /src/colab/local_settings.py file

Change COLAB_TRAC_URL to

.. code-block::

  COLAB_TRAC_URL = 'http://localhost:5000/trac/'

Or the port you're using to Trac

Use fabric at colab's root to update the requirements to your VM

.. code-block::

  fabric runserver:update

*NOTE:*

  The fabric installation on ubuntu through 'pip install' might not be added to the path so you'll need to find
  where it was installed if thats your case

Now simply run fabric again to run the server (it'll also sync and migrate colab's database)

.. code-block::

  fabric runserver

You should be able to see colab with its cms service already working at port 8000(because of vagrant redirects)

*NOTE*

  In case login doesn't work, change the SITE_URL in src/colab/local_settings.py the reflect the django's port
  Also, add the following line riht bellow it
    BROWSERID_AUDIENCES = [SITE_URL, SITE_URL.replace('https', 'http')]

Installing Solr and indexing colab's schemas
==========================================
In Progress of making it readable
  #http servlet jetty
  sudo apt-get install jetty

  #solr
  wget http://ftp.unicamp.br/pub/apache/lucene/solr/4.6.1/solr-4.6.1.tgz
  tar xvzf solr-4.6.1.tgz
  sudo mv solr-4.6.1 /usr/share/solr

  sudo cp /usr/share/solr/example/webapps/solr.war /usr/share/solr/example/solr/solr.war

  python manage.py build_solr_schema >> schema.xml
    #existe mais de uma referencia a stopwords_en
    trocar no schema.xml stopwords_en.txt por lang/stopwords_en.txt

  sudo cp schema.xml /usr/share/solr/example/solr/collection1/conf

  #inclusive a tag
  Remova <updateLog> em solrconfig.xml localizado em /usr/share/solr/example/solr/collection1/conf

  #executa servidor
  cd /usr/share/solr/example/; java -jar start.jar;

  #indexa
  python manage.py update_index