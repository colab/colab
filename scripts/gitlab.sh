#!/bin/bash

#To show the debug log
set -x

DATABASE_HOST=$1

if [[ ! "$DATABASE_HOST" ]]
    then
    echo "Uso: ./gitlab.sh <DATABASE_HOST>"
    exit -1
fi

[ -s "$HOME/.rvm/scripts/rvm" ] && . "$HOME/.rvm/scripts/rvm"

sudo yum install -y wget yum-utils vim

sudo wget -O /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6 https://www.fedoraproject.org/static/0608B895.txt
sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6
 
sudo wget -O /etc/yum.repos.d/PUIAS_6_computational.repo https://gitlab.com/gitlab-org/gitlab-recipes/raw/master/install/centos/PUIAS_6_computational.repo
sudo wget -O /etc/pki/rpm-gpg/RPM-GPG-KEY-puias http://springdale.math.ias.edu/data/puias/6/x86_64/os/RPM-GPG-KEY-puias
sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-puias
sudo yum-config-manager --enable epel --enable PUIAS_6_computational
 
sudo yum -y groupinstall 'Development Tools'
sudo yum -y install readline readline-devel ncurses-devel gdbm-devel glibc-devel tcl-devel openssl-devel curl-devel expat-devel db4-devel byacc sqlite-devel libyaml libyaml-devel libffi libffi-devel libxml2 libxml2-devel libxslt libxslt-devel libicu libicu-devel system-config-firewall-tui redis crontabs logwatch logrotate perl-Time-HiRe postfix zlib-devel perl-CPAN gettext curl-develgettext-devel openssl-devel
 
sudo chkconfig redis on
sudo service redis start

sudo yum -y remove git

mkdir /tmp/git && cd /tmp/git
wget https://git-core.googlecode.com/files/git-1.9.0.tar.gz
tar xzf git-1.9.0.tar.gz
cd git-1.9.0/
./configure
make
sudo make prefix=/usr/local install
 
sudo adduser --system --shell /bin/bash --comment 'GitLab' --create-home --home-dir /home/git/ git

sudo echo 'git ALL=(ALL) ALL' >> /etc/sudoers.d/git
#################################################

#sudo sh -c "curl -L get.rvm.io | bash -s stable"
sudo usermod -a -G rvm git
#source /etc/profile.d/rvm.sh
#sudo -iu git source '/usr/local/rvm/scripts/rvm'
#sudo -iu git rvm install 2.0.0 
#sudo -iu git rvm gemset create gitlab
sudo -iu git rvm use 2.0.0@gitlab --default

#################################################

#sudo -iu git gem install bundler --no-ri --no-rdoc
sudo -iu git /usr/local/bin/git clone https://gitlab.com/gitlab-org/gitlab-shell.git
sudo -iu git /usr/local/bin/git --git-dir=/home/git/gitlab-shell/.git --work-tree=/home/git/gitlab-shell/ reset --hard v1.9.3
sudo -u git cp /home/git/gitlab-shell/config.yml.example /home/git/gitlab-shell/config.yml
sudo -iu git ruby /home/git/gitlab-shell/bin/install
sudo restorecon -Rv /home/git/.ssh

sudo -iu git /usr/local/bin/git clone https://github.com/colab-community/gitlabhq.git -b spb-stable /home/git/gitlab
sudo -u git cp /home/git/gitlab/config/gitlab.yml.example /home/git/gitlab/config/gitlab.yml

sudo -iu git mkdir /home/git/gitlab-satellites
sudo chmod u+rwx,g+rx,o-rwx /home/git/gitlab-satellites
sudo -u git cp /home/git/gitlab/config/unicorn.rb.example /home/git/gitlab/config/unicorn.rb
sudo -u git cp /home/git/gitlab/config/initializers/rack_attack.rb.example /home/git/gitlab/config/initializers/rack_attack.rb
sudo sed -i "s/gitlab_url: \"http:\/\/localhost\/\"/gitlab_url: \"http:\/\/$2:8090\/gitlab\//" /home/git/gitlab-shell/config.yml

sudo -iu git /usr/local/bin/git config --global user.name "GitLab"
sudo -iu git /usr/local/bin/git config --global user.email "gitlab@localhost"
sudo -iu git /usr/local/bin/git config --global core.autocrlf input
sudo chmod o-rwx /home/git/gitlab/config/database.yml
sudo -u git -H bash -c 'echo "production:
  adapter: postgresql
  encoding: unicode
  database: gitlabhq_production
  pool: 10
  username: git
  host: $DATABASE_HOST" > /home/git/gitlab/config/database.yml'

# Baixando as dependencias, criando o banco, instalando de fato
sudo su - git -c 'cd /home/git/gitlab && bundle config build.pg'
sudo su - git -c 'cd /home/git/gitlab && bundle config build.nokogiri --use-system-libraries'
sudo su - git -c 'cd /home/git/gitlab && bundle install --verbose --deployment --without development test mysql aws'
sudo su - git -c 'cd /home/git/gitlab && echo yes | bundle exec rake db:create db:migrate RAILS_ENV=production'
sudo su - git -c 'cd /home/git/gitlab && echo yes | bundle exec rake gitlab:setup RAILS_ENV=production'
sudo su - git -c 'cd /home/git/gitlab bundle exec rake assets:precompile RAILS_ENV=production'

# Configurando o servico do gitlab
sudo wget -O /etc/init.d/gitlab https://gitlab.com/softwarepublico/colabdocumentation/raw/master/Arquivos/gitlab-unicorn
sudo chmod +x /etc/init.d/gitlab
sudo chkconfig --add gitlab
sudo chkconfig gitlab on
sudo cat /home/git/gitlab/lib/support/logrotate/gitlab > /etc/logrotate.d/gitlab
sudo service gitlab restart
