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
            - [Title and Project Name](#title-and-project-name)
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
./manage.py migrate
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

##### Theme and Plugins
Add the theme and plugins it incorporates to `INSTALLED_APPS`:

```py
# List of configuration classes / app packages in order of priority (i.e., the
# first item in the list has final say when collisions occur)
INSTALLED_APPS = (
    # Default
#    'django.contrib.admin',
#    'django.contrib.auth',
#    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Plugins
    # See https://github.com/open-oni?q=plugin for available plugins
    'onisite.plugins.calendar',
    'onisite.plugins.featured_content',
    'onisite.plugins.map',

    # OpenONI
    'django.contrib.humanize',  # Added to make data more human-readable
    'sass_processor',
    'themes.nebraska',
    'themes.default',
    'core',
)
```

##### Title and Project Name
Set the title and project name text for the website

```py
# SITE_TITLE that will be used for display purposes throughout app
# PROJECT_NAME may be the same as SITE_TITLE but can be used
# for longer descriptions that will only show up occasionally
# Example 'Open ONI' for most headers, 'Open Online Newspapers Initiative'
# for introduction / about / further information / etc
SITE_TITLE = "Nebraska Newspapers"
PROJECT_NAME = "Nebraska Newspapers"
```


#### Logging
Create symlink at `/var/log/openoni` to `/var/local/www/django/openoni/log`

```bash
ln -s /var/local/www/django/openoni/log /var/log/openoni
```

#### URLs
Set the URLs file to use the theme and plugins it incorporates

`vim onisite/urls.py`:
```python
from django.conf.urls import url, include
from onisite.plugins.featured_content import views as fc_views

urlpatterns = [
  url(r'^$', fc_views.featured, name="featured_home"),
  url(r'^calendar-', include("onisite.plugins.calendar.urls")),
  url(r'^map', include("onisite.plugins.map.urls")),

  url(r'', include("themes.nebraska.urls")),
  url(r'', include("core.urls")),
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

./manage.py compilescss
./manage.py collectstatic -c

# Grant write access for both Apache and group
sudo chown -R apache static/compiled/
sudo chmod -R g+w static/compiled/
```

## Load Batches
Run these commands as a regular user rather than root

```bash
# Repeat as necessary
./manage.py load_batch /var/local/www/django/openoni/data/batches/(batch_name)/

# Run a script with nohup in the background to ingest multiple batches quietly
nohup (command) >> nohup.out
```

