#!/bin/bash

set -x

### Install solr

curl http://archive.apache.org/dist/lucene/solr/4.10.2/solr-4.10.2.tgz > solr-4.10.2.tgz
tar xf solr-4.10.2.tgz
mv solr-4.10.2 /etc/solr-4.10.2
rm -r solr-4.10.2.tgz
cp /etc/solr-4.10.2/example/solr/collection1/conf/lang/stopwords_en.txt /etc/solr-4.10.2/example/solr/collection1/conf/stopwords_en.txt
chown vagrant:vagrant /etc/solr-4.10.2

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
