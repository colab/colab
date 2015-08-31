#!/bin/bash

set -x

### Configure Colab
export VIRTUALENVWRAPPER_PYTHON="/usr/bin/python2.7"

set +e
if [ -f /usr/local/bin/virtualenvwrapper.sh ]; then
    source /usr/local/bin/virtualenvwrapper.sh
elif [ -f /usr/share/virtualenvwrapper/virtualenvwrapper.sh ]; then
    source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
else
    source /usr/bin/virtualenvwrapper.sh
fi

if [ ! -d /home/vagrant/.virtualenvs/colab ]; then
    mkvirtualenv colab
fi

workon colab
pip install --upgrade setuptools

set -e

for dir in /vagrant/colab /vagrant; do
    if [ -f $dir/setup.py ]; then
        basedir="$dir"
        break
    fi
done
pip install -e $basedir

### Create conf directory
sudo mkdir -p /etc/colab
sudo chown vagrant:vagrant /etc/colab

if [ ! -s /etc/colab/settings.py ]; then
    colab-admin initconfig > /etc/colab/settings.py
    rm -f /etc/colab/settings.pyc  # remove pyc if exists
fi

colab-admin migrate
colab-admin loaddata /vagrant/tests/test_data.json

# Init.d Celery files
sudo cp $basedir/vagrant/misc/etc/init.d/celery* /etc/init.d/
sudo cp $basedir/vagrant/misc/etc/default/celery* /etc/default/
sudo service celeryd stop || echo
sudo service celerybeat stop || echo
sleep 2
sudo service celeryd start
sudo service celerybeat start

colab-admin rebuild_index --noinput
