#! /bin/bash

echo "Make sure rvm is installed at /user/local/rvm"
sudo bash -c "curl -L get.rvm.io | bash -s stable"

echo "Set rvm on the PATH and install ruby 2.0.0"
sudo bash -c "source /usr/local/rvm/scripts/rvm && rvm install ruby-2.0.0"
sudo bash -c "source /usr/local/rvm/scripts/rvm && rvm use 2.0.0 --default"

echo "Create gemsets for gitlab and redmine"
sudo bash -c "source /usr/local/rvm/scripts/rvm && rvm gemset create gitlab"
sudo bash -c "source /usr/local/rvm/scripts/rvm && rvm gemset create redmine"

