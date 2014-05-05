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
  
  
Installing Mailman with Nginx
=============================

Nginx Configuration:

In order to let nginx serve the Mailman web interface, we need to have the fcgiwrap package installed:
  
.. code-block::

  sudo apt-get install fcgiwrap
  
Setting the vhost:
  
Create the www.example.com web site root as follows:

.. code-block::
  
  mkdir -p /var/www/www.example.com/web
  
Next create a basic nginx vhost configuration editing the .vhost file (editor /etc/nginx/sites-available/www.example.com.vhost):
  
.. code-block::
  
  server {
       listen 8000;
       server_name www.example.com example.com;
       root /var/www/www.example.com/web;
       if ($http_host != "localhost:8080") {
                 rewrite ^ localhost$request_uri permanent;
       }
       index index.php index.html;
       location = /favicon.ico {
                log_not_found off;
                access_log off;
       }
       location = /robots.txt {
                allow all;
                log_not_found off;
                access_log off;
       }
       # Deny all attempts to access hidden files such as .htaccess, .htpasswd, .DS_Store (Mac).
       location ~ /\. {
                deny all;
                access_log off;
                log_not_found off;
       }
       location ~*  \.(jpg|jpeg|png|gif|css|js|ico)$ {
                expires max;
                log_not_found off;
       }
  }
  
To enable the vhost, we create a symlink to it from the /etc/nginx/sites-enabled/ directory:

.. code-block::

  cd /etc/nginx/sites-enabled/
  ln -s /etc/nginx/sites-available/www.example.com.vhost www.example.com.vhost

Reload nginx for the changes to take effect:

.. code-block::

  /etc/init.d/nginx reload
  
Mailman Configuration:

.. code-block::

  sudo apt-get install mailman

Create a new mailing list:

.. code-block::

  sudo newlist mailman
  
Open the /etc/aliases (editor /etc/aliases) and add the following:

.. code-block::

  mailman:              "|/var/lib/mailman/mail/mailman post mailman"
  mailman-admin:        "|/var/lib/mailman/mail/mailman admin mailman"
  mailman-bounces:      "|/var/lib/mailman/mail/mailman bounces mailman"
  mailman-confirm:      "|/var/lib/mailman/mail/mailman confirm mailman"
  mailman-join:         "|/var/lib/mailman/mail/mailman join mailman"
  mailman-leave:        "|/var/lib/mailman/mail/mailman leave mailman"
  mailman-owner:        "|/var/lib/mailman/mail/mailman owner mailman"
  mailman-request:      "|/var/lib/mailman/mail/mailman request mailman"
  mailman-subscribe:    "|/var/lib/mailman/mail/mailman subscribe mailman"
  mailman-unsubscribe:  "|/var/lib/mailman/mail/mailman unsubscribe mailman"

Run:

.. code-block::

  sudo newaliases

Now restart postfix and mailman:

.. code-block::

  sudo /etc/init.d/postfix restart
  sudo /etc/init.d/mailman start
  
Open /etc/nginx/sites-available/www.example.com.vhost and add the following part to the server {} container:

.. code-block::

  server {
  [...]
          location /cgi-bin/mailman {
                 root /usr/lib/;
                 fastcgi_split_path_info (^/cgi-bin/mailman/[^/]*)(.*)$;
                 include /etc/nginx/fastcgi_params;
                 fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                 fastcgi_param PATH_INFO $fastcgi_path_info;
                 fastcgi_param PATH_TRANSLATED $document_root$fastcgi_path_info;
                 fastcgi_intercept_errors on;
                 fastcgi_pass unix:/var/run/fcgiwrap.socket;
          }
          location /images/mailman {
                 alias /usr/share/images/mailman;
          }
          location /pipermail {
                 alias /var/lib/mailman/archives/public;
                 autoindex on;
          }
  [...]
  }

Now create the fastcgi_params file and add the following:

.. code-block::

  fastcgi_param	QUERY_STRING		$query_string;
  fastcgi_param	REQUEST_METHOD		$request_method;
  fastcgi_param	CONTENT_TYPE		$content_type;
  fastcgi_param	CONTENT_LENGTH		$content_length;
  
  fastcgi_param	SCRIPT_FILENAME		$document_root$fastcgi_script_name;
  fastcgi_param	SCRIPT_NAME		$fastcgi_script_name;
  fastcgi_param	REQUEST_URI		$request_uri;
  fastcgi_param	DOCUMENT_URI		$document_uri;
  fastcgi_param	DOCUMENT_ROOT		$document_root;
  fastcgi_param	SERVER_PROTOCOL		$server_protocol;
  
  fastcgi_param	GATEWAY_INTERFACE	CGI/1.1;
  fastcgi_param	SERVER_SOFTWARE		nginx;
  
  fastcgi_param	REMOTE_ADDR		$remote_addr;
  fastcgi_param	REMOTE_PORT		$remote_port;
  fastcgi_param	SERVER_ADDR		$server_addr;
  fastcgi_param	SERVER_PORT		$server_port;
  fastcgi_param	SERVER_NAME		$server_name;

Now open the mm_config.py file (sudo editor /etc/mailman/mm_config.py) and modify the lines below to:

.. code-block::

  DEFAULT_EMAIL_HOST = 'localhost'
  DEFAULT_URL_HOST = 'localhost:8080'

To these modifications have effect do the following:

.. code-block::

  sudo withlist -l -a -r fix_url 
  
Also tt's needed to add permission to mailman to access the name_of_the_list.mbox because it needs to archive the emails:

.. code-block::

  sudo chown -R root:list /var/lib/mailman/archives
  sudo chown -R root:list /var/lib/mailman/data/aliases
  sudo chown -R root:list /etc/aliases
  sudo chmod -R u+rwX /var/lib/mailman/archives
  
Now restart fcgi, mailman and nginx:

.. code-block::
  
  sudo /etc/init.d/fcgiwrap restart
  sudo /etc/init.d/mailman restart
  sudo /etc/init.d/nginx reload
  
To see if it's working:

.. code-block::
  
  http://localhost:8080/cgi-bin/mailman/listinfo/mailman
  
Setting up Colab
=========================

You can exit the vagrant VM ('exit' inside the ssh shell) but for now leave it running Trac and start a new terminal tab

Open the /src/colab/local_settings.py file

Change COLAB_TRAC_URL to

.. code-block::

  COLAB_TRAC_URL = 'http://localhost:5000/trac/'

Or the port you're using to Trac

After this it's needed to import the e-mails from Mailman:
  
.. code-block::
  
  sudo python manage.py import_emails
  
And also update Solr:

.. code-block::

  sudo python manage.py update_index

Then, use fabric at colab's root to update the requirements to your VM

.. code-block::

  fabric runserver:update

*NOTE:*

  The fabric installation on ubuntu through 'pip install' might not be added to the path so you'll need to find
  where it was installed if thats your case

Lastly, run fabric again to run the server (it'll also sync and migrate colab's database) and open new tabs to run trac and solr:

.. code-block::

  fab runserver
  fab trac
  fab solr

You should be able to see colab with its cms service already working at port 8000(because of vagrant redirects)

*NOTE*

  In case login doesn't work, change the SITE_URL in src/colab/local_settings.py and in src/colab/custom_settings.py the reflect the django's port
  Also, add the following line riht bellow it
    BROWSERID_AUDIENCES = [SITE_URL, SITE_URL.replace('https', 'http')]
