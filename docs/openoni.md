# OpenONI

**Contents**

- [Dependencies](#dependencies)
- [Install](#install)
    - [Clone OpenONI](#clone-openoni)
    - [SELinux Permissions](#selinux-permissions)
    - [Python Virtual Environment](#python-virtual-environment)
    - [Migrate Database](#migrate-database)
    - [Newspaper Data Symlink](#newspaper-data-symlink)
- [Configure](#configure)
    - [Solr Schema](#solr-schema)
    - [Django](#django)
        - [Local Settings](#local-settings)
        - [Theme and Plugins](#theme-and-plugins)
        - [Logging](#logging)
        - [URLs](#urls)
        - [WSGI Path](#wsgi-path)
- [Compile Static Assets](#compile-static-assets)
- [Load Batches](#load-batches)


## Dependencies
Install [required services](/docs/services/)

`yum install python-virtualenv`


## Install

### Clone OpenONI

```bash
mkdir /var/local/www/django
chgrp webadmins /var/local/www/django
chmod 2775 /var/local/www/django
cd /var/local/www/django
```

Run these commands as a regular user rather than root
```
git clone git@github.com:open-oni/open-oni.git openoni
cd openoni

# We're currently deploying from dev branch for Django 1.11 LTS
git checkout dev
```

### SELinux Permissions
```bash
# Python executables need httpd-executable SELinux context
semanage fcontext -a -t httpd_sys_script_exec_t "/var/local/www/django/openoni/ENV/lib/python2.7/site-packages/.+\.so"

# Static asset path needs Apache write access
mkdir /var/local/www/django/openoni/static/compiled
chown -R apache /var/local/www/django/openoni/static/compiled
chmod -R g+w /var/local/www/django/openoni/static/compiled
semanage fcontext -a -t httpd_sys_rw_content_t "/var/local/www/django/openoni/static/compiled(/.*)?"

restorecon -F -R /var/local/www/django/openoni/
```

### Python Virtual Environment
Run these commands as a regular user rather than root

```bash
cd /var/local/www/django/openoni

# Create and activate Python virtual environment
virtualenv ENV
source ENV/bin/activate

# Update pip and setuptools
pip install -U pip
pip install -U setuptools

# Install / update OpenONI dependencies
pip install -U -r requirements.pip
```

### Migrate Database
Run these commands as a regular user rather than root

```bash
cd /var/local/www/django/openoni
source ENV/bin/activate
manage.py migrate
```

### Newspaper Data Symlink
Run these commands as a regular user rather than root

```bash
cd /var/local/www/django/openoni
source ENV/bin/activate

rm -rf data/batches
ln -s /var/local/newspapers data/batches

./manage.py batches
```


## Configure

### Solr Schema
```bash
cp /var/local/www/django/openoni/docker/solr/schema.xml /var/solr/data/openoni/conf/schema.xml
cp /var/local/www/django/openoni/docker/solr/solrconfig.xml /var/solr/data/openoni/conf/solrconfig.xml
chown -R solr.solr /var/solr/data/openoni

service solr restart
```

### Django

#### Local Settings
```bash
cp settings_local_example.py settings_local.py
```

Follow instructions within for the appropriate deployment environment

#### Theme and Plugins
[Add theme and plugins](/README.md#including-in-the-open-oni-app)

#### Logging
Create symlink at `/var/log/openoni` to `/var/local/www/django/openoni/log`

```bash
ln -s /var/local/www/django/openoni/log /var/log/openoni
```

#### URLs
For development, use example file as is:
```bash
cp onisite/urls_example.py onisite/urls.py
```

For use with Nebraska Theme:

`vim onisite/urls.py`:
```python
from django.conf.urls import url, include

urlpatterns = [
  url(r'^calendar-', include("onisite.plugins.calendar.urls")),
  url(r'^$', include("onisite.plugins.featured_content.urls")),
  url(r'^map', include("onisite.plugins.map.urls")),

  url('', include("themes.nebraska.urls")),
  url('', include("core.urls")),
]
```

#### WSGI Path
`vim onisite/wsgi.py`:
```python
…
#sys.path.append('/opt/openoni')
sys.path.append('/var/local/www/django/openoni')
…
```


## Compile Static Assets
Run these commands as a regular user rather than root

```bash
cd /var/local/www/django/openoni
source ENV/bin/activate
manage.py collectstatic
```

New contents may need Apache ownership set after creation

```bash
chown -R apache /var/local/www/django/openoni/static/compiled
```


## Load Batches
Run these commands as a regular user rather than root

```bash
# Repeat as necessary
./manage.py load_batch /var/local/www/django/openoni/data/batches/(batch_name)/

# Run a script with nohup in the background to ingest multiple batches quietly
nohup (command) >> nohup.out
```

