#!/bin/bash

apt-get install apache2 libapache2-mod-wsgi
apt-get install libxml2-dev libxslt1-dev # lxml
apt-get install libpq-dev # psycopg2

cd /usr/local/src/colab2/
git pull

if [[ $1 == 'deps' ]] ; then
    # com dependencias

    /usr/local/django/colab2/bin/pip install -r /usr/local/src/colab2/requirements.txt -U
fi

/usr/local/django/colab2/bin/python src/manage.py syncdb
/usr/local/django/colab2/bin/python src/manage.py migrate
touch src/colab/wsgi.py
