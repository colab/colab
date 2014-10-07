#!/bin/bash

export VIRTUALENVWRAPPER_PYTHON="/usr/bin/python2.7"

if [ -f /usr/local/bin/virtualenvwrapper.sh ]; then
    source /usr/local/bin/virtualenvwrapper.sh
else
    source /usr/bin/virtualenvwrapper.sh
fi

if [ ! -d /home/vagrant/.virtualenvs/colab ]; then
    mkvirtualenv colab
fi

workon colab

pip install -r /vagrant/requirements.txt
pip install -e /vagrant

if [ ! -s /etc/colab/settings.yaml ]; then
    colab-init-config > /etc/colab/settings.yaml
fi

colab-admin migrate
