#!/bin/bash

source /usr/local/bin/virtualenvwrapper.sh

if [ ! -d /home/vagrant/.virtualenvs/colab ]; then
    mkvirtualenv colab
fi

workon colab

pip install -r /vagrant/requirements.txt
pip install -e /vagrant

if [ ! -f /etc/colab/settings.yaml ]; then
    colab-init-config > /etc/colab/settings.yaml
fi

colab-admin migrate
