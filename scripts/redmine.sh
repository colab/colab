#!/bin/bash

set -x

if [ ! "$1" ]
  then
      echo "Por favor, passe como parâmetro o ip do banco de dados"
      echo "./redmine.sh 127.0.0.1"
      exit -1
fi

sudo rpm -iUvh https://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm

sudo yum -y install zlib-devel curl-devel httpd-devel apr-devel apr-util-devel subversion git postgresql-devel gcc gcc-c++.x86_64 make automake autoconf curl-devel openssl-devel httpd-devel apr-devel apr-util-devel sqlite-devel libxslt-devel libxml2-devel.x86_64 php-pear ImageMagick ImageMagick-devel ImageMagick-perl vim patch readline readline-devel zlib  libffi-devel make bzip2 libtool bison wget libyaml-devel


curl -L get.rvm.io | bash -s stable

source /etc/profile.d/rvm.sh


rvm install 2.0.0
rvm use 2.0.0 --default

rvm gemset create redmine
rvm gemset use redmine

sudo chown -R $USER: /opt

cd /opt
git clone https://github.com/redmine/redmine.git --branch 2.3-stable

cd /opt/redmine
bundle install --verbose --without mysql sqlite
gem install unicorn --no-ri --no-rdoc
gem install pg -v '0.17.1' --no-ri --no-rdoc

cd config/

echo "production:
  adapter: postgresql
  database: redmine
  host: $1
  username: redmine
  password: redmine
  encoding: utf8" > database.yml


rake generate_secret_token

RAILS_ENV=production rake db:migrate

echo "pt-BR" | RAILS_ENV=production rake redmine:load_default_data


cd /opt/redmine
mkdir pids
wget https://gitlab.com/softwarepublico/colabdocumentation/raw/master/Arquivos/redmine/unicorn.rb -O config/unicorn.rb

wget https://gitlab.com/softwarepublico/colabdocumentation/raw/master/Arquivos/redmine/routes.rb -O config/routes.rb

ln -s /opt/redmine/public /opt/redmine/public/redmine

cd /opt/redmine/plugins
git clone https://github.com/backlogs/redmine_backlogs.git 

cd redmine_backlogs
git checkout v1.0.6

RAILS_ENV=production
export RAILS_ENV
bundle install --verbose

gem uninstall rack -v '1.5.2'

cd /opt/redmine
bundle install --verbose --without mysql sqlite
bundle exec rake db:migrate
bundle exec rake redmine:backlogs:install story_trackers=2 task_tracker=1

cd /opt/redmine/plugins
git clone https://github.com/colab-community/single_auth.git

unicorn_rails -c /opt/redmine/config/unicorn.rb -E production -p 9080 -D
