.. -*- coding: utf-8 -*-

.. highlight:: rest

.. _colab_software:

====================
Colab on Cent OS 6.4
====================

Nginx 1.6
=========

Download the nginx

.. code-block::
    cd /tmp
    wget http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm
    sudo rpm -ivh nginx-release-centos-6-0.el6.ngx.noarch.rpm

Install nginx

.. code-block::

    sudo yum install nginx -y

Start nginx with the system

.. code-block::

    sudo chkconfig nginx on


Postgres Server 9.3
===================

Install postgresql

.. code-block::

    sudo yum localinstall http://yum.postgresql.org/9.3/redhat/rhel-6-x86_64/pgdg-centos93-9.3-1.noarch.rpm -y
    sudo yum install postgresql93 postgresql93-devel postgresql93-libs postgresql93-server -y

Initialize database

.. code-block::

    sudo service postgresql-9.3 initdb

Start postgresql with the system

.. code-block::

    sudo chkconfig postgresql-9.3 on

Start postgresql

.. code-block::

    sudo service postgresql-9.3 start

Put the binaries of postgres in the PATH variable

.. code-block::

    echo "export PATH=$PATH:/usr/pgsql-9.3/bin/" >> ~/.bashrc
    source ~/.bashrc
    sudo su
    echo "export PATH=$PATH:/usr/pgsql-9.3/bin/" >> ~/.bashrc
    source ~/.bashrc
    exit

Edit sudoers file

.. code-block::

    sudo vim /etc/sudoers
    
Inside sudoers file change the line

.. code-block::

    Defaults    secure_path = /sbin:/bin:/usr/sbin:/usr/bin
    
To this line

.. code-block::

    Defaults    secure_path = /sbin:/bin:/usr/sbin:/usr/bin:/usr/pgsql-9.3/bin/

And save the file

.. code-block::

    [ESC]:wq!

Create a password for postgresql database, in this case we have an user called ``colab``, and we  will set its password too.

.. code-block::

    sudo -u postgres psql
    
.. code-block::

    ALTER USER postgres WITH PASSWORD 'colab';
    CREATE USER colab SUPERUSER INHERIT CREATEDB CREATEROLE;
    ALTER USER colab PASSWORD 'colab';
    \q
    
Restart the postgresql

.. code-block::

    sudo service postgresql-9.3 restart


Trac 1.0
========

Install the dependencies

.. code-block::

    sudo yum install gcc python-devel python-setuptools -y
    
Install this package to use Trac with postgresql

.. code-block::

    sudo easy_install psycopg2
    
If you are going to use postgresql, create the database for trac

.. code-block::

    sudo -u postgres psql

.. code-block::

    	CREATE DATABASE "trac_colab" WITH OWNER "colab" ENCODING 'UTF8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8' TEMPLATE=template0;
    	\q

And change the database authentication to md5

.. code-block::

    sudo vi /var/lib/pgsql/9.3/data/pg_hba.conf
    
.. code-block::

    [ESC]:%s/peer/md5
    [ESC]:%s/ident/md5

.. code-block::

    [ESC]:wq!
    	
And restart postgresql

.. code-block::

    sudo service postgresql-9.3 restart
    
    
Install Trac

.. code-block::

    sudo easy_install trac

Intiate Trac

.. code-block::

    sudo mkdir -p /opt/trac
    sudo trac-admin /opt/trac initenv
    
In ``Project Name [My Project]>`` we used ``colab``. And if you are going to use the postgresql, put this line in ``Database connection string [sqlite:db/trac.db]>``, and we are using the user ``colab``.

.. code-block::

	postgres://colab:colab@/trac_colab?host=localhost

SVN Plugin

Install subversion

.. code-block::

    sudo yum install subversion -y
    
Create a repository and initiate it

.. code-block::

    mkdir -p /home/colab/myrepo
    mkdir -p /tmp/project/{branches,tags,trunk}
    svnadmin create /home/colab/myrepo/
    svn import /tmp/project file:///home/colab/myrepo/ -m "initial import"
    sudo rm -rf /tmp/project
    find /home/colab/myrepo -type f -exec chmod 660 {} \;
    find /home/colab/myrepo -type d -exec chmod 2770 {} \;

Edit the Trac's configuration file

.. code-block::

    sudo vim /opt/trac/conf/trac.ini
    
Inside the trac.ini file.
Replace the line

.. code-block::

    repository_dir = 
    
With this one

.. code-block::

    repository_dir = /home/colab/myrepo/
    
Insert those lines in the end of file to activate the view of subversion on Trac.

.. code-block::

    [components]
    tracopt.versioncontrol.svn.* = enabled

.. code-block::

    [ESC]:wq!

Remote User

Create the plugin to set the remote user variable

.. code-block::

    sudo vim /opt/trac/plugins/remote-user-auth.py
    
And put this in the file

.. code-block::

    from trac.core import *
    from trac.config import BoolOption
    from trac.web.api import IAuthenticator
    
    class MyRemoteUserAuthenticator(Component):
    
        implements(IAuthenticator)
    
        obey_remote_user_header = BoolOption('trac', 'obey_remote_user_header', 'false',
                   """Whether the 'Remote-User:' HTTP header is to be trusted for user logins 
                    (''since ??.??').""")
    
        def authenticate(self, req):
            if self.obey_remote_user_header and req.get_header('Remote-User'):
                return req.get_header('Remote-User')
            return None

Save the file

.. code-block::

    [ESC]:wq!

Edit Trac's configuration file

.. code-block::

    sudo vim /opt/trac/conf/trac.ini
    
Insert this line in the [trac] session.

.. code-block::
    
    obey_remote_user_header = true

Save and quit
    
.. code-block::

    [ESC]:wq!

*NOTE:*
    To run Trac: ``sudo tracd --port 5000 /opt/trac`` . And to access it `http://localhost:5000 <http://localhost:5000>`_ 

Solr 4.6.1
==========

Download Solr and unpack it

.. code-block::

    cd /tmp
    sudo wget http://archive.apache.org/dist/lucene/solr/4.6.1/solr-4.6.1.tgz
    sudo tar xvzf solr-4.6.1.tgz
    
Install Solr in ``/usr/share``
    
.. code-block::

    sudo mv solr-4.6.1 /usr/share/solr
    sudo cp /usr/share/solr/example/webapps/solr.war /usr/share/solr/example/solr/solr.war

Remove the ``updateLog`` tag, editing the solrconfig.xml

.. code-block::

    sudo vim /usr/share/solr/example/solr/collection1/conf/solrconfig.xml
    
And remove those lines

.. code-block::

    <updateLog>
      <str name="dir">${solr.ulog.dir:}</str>
    </updateLog>
    
.. code-block::

    [ESC]wq!

*NOTE:*

    To run Solr
        cd /usr/share/solr/example/; sudo java -jar start.jar

Mailman
=======

Install the fcgiwrap

.. code-block::

    sudo yum install fcgi-devel git -y
    cd /tmp
    sudo git clone https://github.com/gnosek/fcgiwrap.git
    cd fcgiwrap
    sudo yum groupinstall "Development tools" -y
    sudo autoreconf -i
    sudo ./configure
    sudo make
    sudo make install

Now you can install spawn fcgi

.. code-block::

    sudo yum install spawn-fcgi -y
    
And edit the spawn-fgci configuration file

.. code-block::

    sudo vim /etc/sysconfig/spawn-fcgi

.. code-block::

    FCGI_SOCKET=/var/run/fcgiwrap.socket
    FCGI_PROGRAM=/usr/local/sbin/fcgiwrap
    FCGI_USER=apache
    FCGI_GROUP=apache
    FCGI_EXTRA_OPTIONS="-M 0770"
    OPTIONS="-u $FCGI_USER -g $FCGI_GROUP -s $FCGI_SOCKET -S $FCGI_EXTRA_OPTIONS -F 1 -P /var/run/spawn-fcgi.pid -- $FCGI_PROGRAM"

Save and quit
    
.. code-block::

    [ESC]:wq!

Add nginx to the apache's user group, to grant all the right permissions to spawn-fcgi

.. code-block::

    sudo usermod -a -G apache nginx
    
Put spaw-fcgi to start with the system, and start it

.. code-block::

    sudo chkconfig --levels 235 spawn-fcgi on
    sudo /etc/init.d/spawn-fcgi start

Install mailman

.. code-block::

    sudo yum install mailman -y
    
Create a list, in this case we called it ``mailman``

.. code-block::

    sudo /usr/lib/mailman/bin/newlist mailman

Put a real email in ``Enter the email of the person running the list:``. And put a password in ``Initial mailman password:``, we used ``admin`` as password.
    
And add that list to the aliases file

.. code-block::

    sudo vim /etc/aliases
    
.. code-block::

    ## mailman mailing list
    mailman:              "|/usr/lib/mailman/mail/mailman post mailman"
    mailman-admin:        "|/usr/lib/mailman/mail/mailman admin mailman"
    mailman-bounces:      "|/usr/lib/mailman/mail/mailman bounces mailman"
    mailman-confirm:      "|/usr/lib/mailman/mail/mailman confirm mailman"
    mailman-join:         "|/usr/lib/mailman/mail/mailman join mailman"
    mailman-leave:        "|/usr/lib/mailman/mail/mailman leave mailman"
    mailman-owner:        "|/usr/lib/mailman/mail/mailman owner mailman"
    mailman-request:      "|/usr/lib/mailman/mail/mailman request mailman"
    mailman-subscribe:    "|/usr/lib/mailman/mail/mailman subscribe mailman"
    mailman-unsubscribe:  "|/usr/lib/mailman/mail/mailman unsubscribe mailman"

.. code-block::

    [ESC]:wq!

Now, reset the aliases

.. code-block::

    sudo newaliases
    
Restart postfix

.. code-block::

    sudo /etc/init.d/postfix restart
    
And add the mailman to start with the system

.. code-block::

    sudo chkconfig --levels 235 mailman on

Start mailman and create a symbolic link inside cgi-bin

.. code-block::

    sudo /etc/init.d/mailman start
    cd /usr/lib/mailman/cgi-bin/
    sudo ln -s ./ mailman

Create a config file to mailman inside nginx

.. code-block::

    sudo vim /etc/nginx/conf.d/list.conf
    
.. code-block::

    server {
            server_name localhost;
            listen 8080;
    
            location /mailman/cgi-bin {
                   root /usr/lib;
                   fastcgi_split_path_info (^/mailman/cgi-bin/[^/]*)(.*)$;
                   include /etc/nginx/fastcgi_params;
                   fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                   fastcgi_param PATH_INFO $fastcgi_path_info;
                   fastcgi_param PATH_TRANSLATED $document_root$fastcgi_path_info;
                   fastcgi_intercept_errors on;
                   fastcgi_pass unix:/var/run/fcgiwrap.socket;
            }
            location /images/mailman {
                   alias /usr/lib/mailman/icons;
            }
            location /pipermail {
                   alias /var/lib/mailman/archives/public;
                   autoindex on;
            }
    }

.. code-block::

    [ESC]:wq!

Restart nginx to update the new configuration

.. code-block::

    sudo service nginx restart

Edit the config script of mailman, to fix the url used by it.

.. code-block::

    sudo vim /etc/mailman/mm_cfg.py

Add this line in the end of file

.. code-block::

    DEFAULT_URL_PATTERN = 'https://%s/mailman/cgi-bin/'
    
.. code-block::

    [ESC]:wq!
    
Run the fix_url and restart mailman.
    
.. code-block::

    sudo /usr/lib/mailman/bin/withlist -l -a -r fix_url
    sudo service mailman restart

*NOTE:*
    You can access mailman in this url: `http://localhost:8080/mailman/cgi-bin/listinfo <http://localhost:8080/mailman/cgi-bin/listinfo>`_ 


Python 2.7 + Django 1.6
=======================

Install the devel tools to build specific python 2.7 modules

.. code-block::

    sudo yum groupinstall "Development tools" -y
    sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel libxslt-devel -y

Download and compile Python 2.7

.. code-block::

    cd /tmp
    sudo wget --no-check-certificate https://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz
    sudo tar xf Python-2.7.6.tar.xz
    cd Python-2.7.6
    sudo ./configure --prefix=/usr/local
    sudo make
    
Install python 2.7 as an alternative python, because cent os uses python 2.6 in the system.
    
.. code-block::

    sudo make altinstall

Update the PATH variable to execute python as root.

.. code-block::

    sudo su
    echo "export PATH=$PATH:/usr/local/bin/" >> ~/.bashrc
    source ~/.bashrc
    exit

Install the easy_install for python 2.7

.. code-block::

    cd /tmp
    sudo wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
    sudo /usr/local/bin/python2.7 ez_setup.py
    
Instal pip 2.7

.. code-block::

    sudo /usr/local/bin/easy_install-2.7 pip

Install additional packages to python.

.. code-block::

    sudo yum remove libevent -y
    sudo yum install mercurial libevent-devel python-devel -y

Edit sudores file to let ``python2.7`` execute in sudo mode. 

*NOTE:*

    The path ``/usr/bin:/usr/pgsql-9.3/bin/`` will be only in this file if you installed postgresql before, if you didn't just remove it from those lines.

.. code-block::

    sudo vim /etc/sudoers

Change the line

.. code-block::

    Defaults    secure_path = /sbin:/bin:/usr/sbin:/usr/bin:/usr/pgsql-9.3/bin/
    
To

.. code-block::

    Defaults    secure_path = /sbin:/bin:/usr/sbin:/usr/bin:/usr/pgsql-9.3/bin/:/usr/local/bin/
    
.. code-block::

    [ESC]:wq!
    
Django 1.6

Install django and uwsgi

.. code-block::

    sudo pip2.7 install django
    sudo pip2.7 install uwsgi

Colab
=====

Install git and clone colab

.. code-block::

    sudo yum install git -y
    cd /opt
    sudo git clone https://github.com/colab-community/colab.git
    
Install colab requirements

.. code-block::

    sudo pip2.7 install mimeparse
    sudo pip2.7 install -r /opt/colab/requirements.txt
    sudo pip2.7 uninstall django_browserid -y
    sudo pip2.7 install django_browserid==0.9

    
Create the local_settings file in colab folder

.. code-block::

    sudo cp /opt/colab/src/colab/local_settings-dev.py /opt/colab/src/colab/local_settings.py

And edit it inserting browser id in the end of file

.. code-block::

    sudo vim /opt/colab/src/colab/local_settings.py
    
.. code-block::

    BROWSERID_AUDIENCES = [SITE_URL, SITE_URL.replace('https', 'http')]
    
.. code-block::

    [ESC]:wq!
    
Create the database for colab, remind that the user colab was created at the postgresql section

.. code-block::

    sudo -u postgres psql
    
.. code-block::

    CREATE DATABASE "colab" WITH OWNER "colab" ENCODING 'UTF8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8' TEMPLATE=template0;
    \q


Build the solr schema.xml

.. code-block::

    cd /opt/colab/src
    sudo su
    python2.7 manage.py build_solr_schema > /opt/colab/src/schema.xml
    exit

Copy the shcema to solr

.. code-block::

    sudo cp /opt/colab/src/schema.xml /usr/share/solr/example/solr/collection1/conf/schema.xml
    sudo rm -f /opt/colab/src/schema.xml

Edit the schema to change the ``stopwords_en.txt`` to ``lang/stopwords_en.txt``

.. code-block::

    sudo vim /usr/share/solr/example/solr/collection1/conf/schema.xml

.. code-block::

    [ESC]:%s/stopwords_en.txt/lang\/stopwords_en.txt
    [ESC]:wq!


Syncronize and migrate the colab's database

.. code-block::

    cd /opt/colab/src
    python2.7 manage.py syncdb
    python2.7 manage.py migrate

Start Solr in a terminal, and then, in other terminal, update colab index

.. code-block::

        cd /opt/colab/src
        python2.7 manage.py update_index

Now you can close this terminal, and stop solr with ``Ctrl+C``

Import mailman e-mails

.. code-block::

    sudo python2.7 /opt/colab/src/manage.py import_emails

*NOTE:*

    To run Colab: python2.7 /opt/colab/src/manage.py runserver . To access colab go in: `http://localhost:8000 <http://localhost:8000>`_