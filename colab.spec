%define name colab
%define version 2.0a3
%define unmangled_version 2.0a3
%define release 3
%define buildvenv /var/tmp/%{name}-%{version}

Summary: Collaboration platform for communities
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPLv2
Group: Development/Tools
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
Vendor: Sergio Oliveira <sergio@tracy.com.br>
Url: https://github.com/colab-community/colab
BuildArch: noarch
BuildRequires: colab-deps, python-virtualenv
Requires: colab-deps, solr, mailman-api

%description
Integrated software development platform.

%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
# install colab into virtualenv to make sure dependencies are OK
rm -rf %{buildvenv}
cp -r /usr/lib/colab %{buildvenv}
PATH=%{buildvenv}/bin:$PATH pip install --no-index .
virtualenv --relocatable %{buildvenv}

# cleanup virtualenv
rpm -ql colab-deps | sed '/^\/usr\/lib\/colab\// !d; s#/usr/lib/colab/##' > cleanup.list
while read f; do
  if [ -f "%{buildvenv}/$f" ]; then
    rm -f "%{buildvenv}/$f"
  fi
done < cleanup.list
rm -f cleanup.list
find %{buildvenv} -type d -empty -delete

%install
mkdir -p %{buildroot}/etc/colab
mkdir -p %{buildroot}/usr/lib

mkdir -p %{buildroot}/usr/share/nginx/
ln -s /var/lib/colab-assets %{buildroot}/usr/share/nginx/colab

# install virtualenv
rm -rf %{buildroot}/usr/lib/colab
cp -r %{buildvenv} %{buildroot}/usr/lib/colab
mkdir -p %{buildroot}/%{_bindir}
cat > %{buildroot}/%{_bindir}/colab-admin <<EOF
#!/bin/sh
set -e

if [ "\$USER" = colab ]; then
  exec /usr/lib/colab/bin/colab-admin "\$@"
else
  exec sudo -u colab /usr/lib/colab/bin/colab-admin "\$@"
fi
EOF
chmod +x %{buildroot}/%{_bindir}/colab-admin

# install initscript
install -d -m 0755 %{buildroot}/lib/systemd/system
install -m 0644 misc/lib/systemd/system/colab.service %{buildroot}/lib/systemd/system
# install crontab
install -d -m 0755 %{buildroot}/etc/cron.d
install -m 0644 misc/etc/cron.d/colab %{buildroot}/etc/cron.d

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %{buildvenv}

%files
/usr/lib/colab
%{_bindir}/*
/etc/cron.d/colab
/lib/systemd/system/colab.service
/usr/share/nginx/colab

%post
groupadd colab || true
if ! id colab; then
  useradd --system --gid colab  --home-dir /usr/lib/colab --no-create-home colab
fi

usermod --append --groups mailman colab

mkdir -p /etc/colab

if [ ! -f /etc/colab/settings.yaml ]; then
  SECRET_KEY=$(openssl rand -hex 32)
  cat > /etc/colab/settings.yaml <<EOF
## Set to false in production
DEBUG: true
TEMPLATE_DEBUG: true

## System admins
ADMINS: &admin
-
  - John Foo
  - john@example.com
-
  - Mary Bar
  - mary@example.com

MANAGERS: *admin

COLAB_FROM_ADDRESS: '"Colab" <noreply@example.com>'
SERVER_EMAIL: '"Colab" <noreply@example.com>'

EMAIL_HOST: localhost
EMAIL_PORT: 25
EMAIL_SUBJECT_PREFIX: '[colab]'

SECRET_KEY: '$SECRET_KEY'

SITE_URL: 'http://localhost:8000'
BROWSERID_AUDIENCES:
- http://localhost:8000
#  - http://example.com
#  - https://example.org
#  - http://example.net

ALLOWED_HOSTS:
- localhost
#  - example.com
#  - example.org
#  - example.net

## Disable indexing
ROBOTS_NOINDEX: false

#PROXIED_APPS:
#   gitlab:
#     upstream: 'http://localhost:8080/gitlab/'

## Enabled BROWSER_ID protocol
#  BROWSERID_ENABLED: True
EOF
  chown root:colab /etc/colab/settings.yaml
  chmod 0640 /etc/colab/settings.yaml
fi

mkdir -p /etc/colab/settings.d

if [ ! -f /etc/colab/settings.d/00-database.yaml ]; then
  cat > /etc/colab/settings.d/00-database.yaml <<EOF
DATABASES:
default:
  ENGINE: django.db.backends.postgresql_psycopg2
  NAME: colab
  USER: colab
  HOST: localhost
  PORT: 5432
EOF
  chown root:colab /etc/colab/settings.d/00-database.yaml
  chmod 0640 /etc/colab/settings.d/00-database.yaml
fi


# only applies if there is a local PostgreSQL server
if [ -x /usr/bin/postgres ]; then

  # start/enable the service
  postgresql-setup initdb || true
  systemctl start postgresql
  systemctl enable postgresql

  if [ "$(sudo -u postgres -i psql --quiet --tuples-only -c "select count(*) from pg_user where usename = 'colab';")" -eq 0 ]; then
    # create user
    sudo -u postgres -i createuser colab
  fi

  if [ "$(sudo -u postgres -i psql --quiet --tuples-only -c "select count(1) from pg_database where datname = 'colab';")" -eq 0 ]; then
    # create database
    sudo -u postgres -i createdb --owner=colab colab
  fi

  colab-admin migrate
fi

mkdir -p /var/lib/colab-assets
chown colab:colab /var/lib/colab-assets

mkdir -p /var/lock/colab
chown colab:colab /var/lock/colab

if [ -f /etc/colab/settings.yaml ]; then
  yes yes | colab-admin collectstatic
fi

