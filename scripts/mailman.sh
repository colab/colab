#!/bin/sh

set -x

if [[ ! "$1" || ! "$2" ]]
        then
        echo " Parametros nao encontrados."
        echo " ./mailman.sh <ADMIN_MAIL> <ADMIN_PASSWD> "
        exit -1
fi

LIST_NAME="mailman"
ADMIN_MAIL=$1
ADMIN_PASSWD=$2

sudo rpm -Uvh https://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm

sudo echo '[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/centos/6/$basearch/
gpgcheck=0
enabled=1' > /etc/yum.repos.d/nginx.repo

sudo yum install nginx wget fcgi-devel git -y
sudo chkconfig nginx on

cd /tmp
sudo git clone https://github.com/gnosek/fcgiwrap.git
sudo yum groupinstall "Development tools" -y
cd /tmp/fcgiwrap
sudo autoreconf -i
sudo ./configure
sudo make && make install

sudo yum install spawn-fcgi -y

sudo sh -c "echo 'FCGI_SOCKET=/var/run/fcgiwrap.socket' >> /etc/sysconfig/spawn-fcgi"
sudo sh -c "echo 'FCGI_PROGRAM=/usr/local/sbin/fcgiwrap' >> /etc/sysconfig/spawn-fcgi"
sudo sh -c "echo 'FCGI_USER=apache' >> /etc/sysconfig/spawn-fcgi"
sudo sh -c "echo 'FCGI_GROUP=apache' >> /etc/sysconfig/spawn-fcgi"
sudo sh -c "echo 'FCGI_EXTRA_OPTIONS=\"-M 0770\"' >> /etc/sysconfig/spawn-fcgi"
sudo sh -c "echo 'OPTIONS=\"-u \$FCGI_USER -g \$FCGI_GROUP -s \$FCGI_SOCKET -S \$FCGI_EXTRA_OPTIONS -F 1 -P /var/run/spawn-fcgi.pid -- \$FCGI_PROGRAM\"' >> /etc/sysconfig/spawn-fcgi"

sudo yum install mailman -y

echo | sudo /usr/lib/mailman/bin/newlist $LIST_NAME $ADMIN_MAIL $ADMIN_PASSWD

sudo sh -c "echo   >> /etc/aliases"
sudo sh -c "echo '##$LIST_NAME mailing list'  >> /etc/aliases"
sudo sh -c "echo '$LIST_NAME:              \"|/usr/lib/mailman/mail/mailman post $LIST_NAME\"' >> /etc/aliases"
sudo sh -c "echo '$LIST_NAME-admin:        \"|/usr/lib/mailman/mail/mailman admin $LIST_NAME\"' >> /etc/aliases"
sudo sh -c "echo '$LIST_NAME-bounces:      \"|/usr/lib/mailman/mail/mailman bounces $LIST_NAME\"' >> /etc/aliases"
sudo sh -c "echo '$LIST_NAME-confirm:      \"|/usr/lib/mailman/mail/mailman confirm $LIST_NAME\"' >> /etc/aliases"
sudo sh -c "echo '$LIST_NAME-join:         \"|/usr/lib/mailman/mail/mailman join $LIST_NAME\"' >> /etc/aliases"
sudo sh -c "echo '$LIST_NAME-leave:        \"|/usr/lib/mailman/mail/mailman leave $LIST_NAME\"' >> /etc/aliases"
sudo sh -c "echo '$LIST_NAME-owner:        \"|/usr/lib/mailman/mail/mailman owner $LIST_NAME\"' >> /etc/aliases"
sudo sh -c "echo '$LIST_NAME-request:      \"|/usr/lib/mailman/mail/mailman request $LIST_NAME\"' >> /etc/aliases"
sudo sh -c "echo '$LIST_NAME-subscribe:    \"|/usr/lib/mailman/mail/mailman subscribe $LIST_NAME\"' >> /etc/aliases"
sudo sh -c "echo '$LIST_NAME-unsubscribe:  \"|/usr/lib/mailman/mail/mailman unsubscribe $LIST_NAME\"' >> /etc/aliases"

sudo newaliases

sudo yum -y install postfix

sudo /etc/init.d/postfix restart

sudo chkconfig --levels 235 mailman on

sudo /etc/init.d/mailman start 
cd /usr/lib/mailman/cgi-bin/
sudo ln -s ./ mailman

sudo wget https://gitlab.com/softwarepublico/colabdocumentation/raw/master/Arquivos/mailman/list.conf -O /etc/nginx/conf.d/list.conf

sudo service nginx restart

sudo sh -c "echo 'DEFAULT_URL_PATTERN = \"https://%s/mailman/cgi-bin/\"' >> /etc/mailman/mm_cfg.py"

sudo /usr/lib/mailman/bin/withlist -l -a -r fix_url
sudo service mailman restart

sudo usermod -a -G apache nginx

sudo chkconfig --levels 235 spawn-fcgi on
sudo /etc/init.d/spawn-fcgi start

sudo service mailman restart
sudo service nginx restart

