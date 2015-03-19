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

export SOLR_VERSION=4.10.3
export SOLR_CONFS="/tmp/schema.xml"

$basedir/ci/install_solr.sh
/home/vagrant/solr-4.10.3/bin/solr stop -p 8983

# Init.d Solr files
sudo cp $basedir/vagrant/misc/etc/init.d/solr /etc/init.d/
cp $basedir/vagrant/solr/start.sh /home/vagrant/solr-$SOLR_VERSION
sudo chkconfig --add solr
sudo service solr start

colab-admin rebuild_index --noinput
