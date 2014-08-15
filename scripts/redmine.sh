#!/bin/bash

LOCAL_HOST=$1
if [ -e $LOCAL_HOST ]; then
    echo "Please, inform the IP address Redmine will be listening"
    echo "ex: ./redmine.sh 127.0.0.1"
    exit -1
fi

echo "Installing a lot of system dependencies also making use of EPEL repository"
sudo rpm -iUvh https://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
sudo yum -y install zlib-devel curl-devel httpd-devel apr-devel apr-util-devel subversion git postgresql-devel gcc gcc-c++.x86_64 make automake autoconf curl-devel openssl-devel httpd-devel apr-devel apr-util-devel sqlite-devel libxslt-devel libxml2-devel.x86_64 php-pear ImageMagick ImageMagick-devel ImageMagick-perl vim patch readline readline-devel zlib  libffi-devel make bzip2 libtool bison wget libyaml-devel

echo "Making sure $USER can access /opt"
sudo chown $USER /opt && cd /opt

echo "Downloading Redmine 2.3"
git clone https://github.com/redmine/redmine.git --branch 2.3-stable && cd /opt/redmine
ln -s /opt/redmine/public /opt/redmine/public/redmine

echo "Installing Ruby/Redmine dependencies, this will take a VERY LONG TIME, grab a cup of coffee..."
rvm gemset use redmine
bundle install --verbose --without mysql sqlite
gem --verbose install unicorn --no-ri --no-rdoc
gem --verbose install pg -v '0.17.1' --no-ri --no-rdoc

echo "Setting Redmine database file"
cd config/ && echo "production:
  adapter: postgresql
  database: redmine
  host: $LOCAL_HOST
  username: redmine
  password: redmine
  encoding: utf8" > database.yml

echo "Initializing Redmine database"
export RAILS_ENV=production 
rake generate_secret_token
rake db:migrate
echo "pt-BR" | rake redmine:load_default_data

echo "Downloading Redmine plugins"
cd /opt/redmine/plugins && git clone https://github.com/colab-community/single_auth.git
cd /opt/redmine/plugins && git clone https://github.com/backlogs/redmine_backlogs.git 

echo "Installing backlogs plugin"
cd redmine_backlogs && git checkout v1.0.6
bundle install --verbose
gem uninstall rack -v '1.5.2'

echo "Finishing Redmine settings"
cd /opt/redmine
bundle install --verbose --without mysql sqlite
bundle exec rake db:migrate
bundle exec rake redmine:backlogs:install story_trackers=2 task_tracker=1

echo "Downloading server configuration files"
cd /opt/redmine && mkdir pids
wget https://gitlab.com/softwarepublico/colabdocumentation/raw/master/Arquivos/redmine/unicorn.rb -O config/unicorn.rb
wget https://gitlab.com/softwarepublico/colabdocumentation/raw/master/Arquivos/redmine/routes.rb -O config/routes.rb

echo "Setting up initialization on supervisor"
if [ -e `cat /etc/supervisord.conf | grep redmine` ]; then
    CMD="source /usr/local/rvm/scripts/rvm &&";
    CMD="$CMD rvm gemset use redmine &&";
    CMD="$CMD unicorn_rails -c /opt/redmine/config/unicorn.rb -E $RAILS_ENV -p 9080 -D";

    echo "[program:redmine]" >> /etc/supervisord.conf;
    echo "command=$CMD" >> /etc/supervisord.conf;
    echo "user=$USER" >> /etc/supervisord.conf;
fi

echo "Finished installing, starting Redmine service"
supervisorctl start redmine

