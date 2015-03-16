#!/bin/bash

set -x

### Configure Colab
export VIRTUALENVWRAPPER_PYTHON="/usr/bin/python2.7"

set +e
if [ -f /usr/local/bin/virtualenvwrapper.sh ]; then
    source /usr/local/bin/virtualenvwrapper.sh
else
    source /usr/bin/virtualenvwrapper.sh
fi

if [ ! -d /home/vagrant/.virtualenvs/colab ]; then
    mkvirtualenv colab
fi

workon colab
set -e

for dir in /vagrant/colab /vagrant; do
    if [ -f $dir/setup.py ]; then
        basedir="$dir"
        break
    fi
done
pip install -e $basedir

if [ ! -s /etc/colab/settings.yaml ]; then
    colab-init-config > /etc/colab/settings.yaml
fi

colab-admin migrate
colab-admin loaddata /vagrant/tests/test_data.json

### Install solr
colab-admin build_solr_schema -f /tmp/schema.xml
curl -sSL https://raw.githubusercontent.com/moliware/travis-solr/master/travis-solr.sh | SOLR_VERSION=4.10.3 SOLR_CONFS="/tmp/schema.xml /vagrant/vagrant/solr-config/stopwords.txt" bash
