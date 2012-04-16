#!/bin/bash

cd /usr/local/src/colab/
hg pull
hg up
rm -fR dist/
python setup.py sdist

if [[ $1 == 'deps' ]] ; then
    # com dependencias
    /usr/local/django/colab/bin/pip install dist/*.gz -U
else
    # sem dependencias
    /usr/local/django/colab/bin/pip install dist/*.gz -U --no-deps
fi

/usr/local/django/colab/bin/python colab/manage.py syncdb
/usr/local/django/colab/bin/python colab/manage.py migrate
touch /usr/local/django/colab/wsgi/colab.wsgi
