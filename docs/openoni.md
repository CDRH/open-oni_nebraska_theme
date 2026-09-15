# Open ONI

## Dependencies
Install [required services](/docs/services/)

`dnf install gcc python3.14-devel`

## Install

Install cifs software to enable mounting network file shares

```bash
dnf install cifs-utils
```

```bash
# Create nebnews group
groupadd nebnews

# Add users to nebnews group
vim /etc/group
```

Add sudoers drop-in config to allow `nebnews` group members to mount
cifs / Samba file shares

`sudo vim /etc/sudoers.d/50-nebnews`

```
# nebnews group members may sudo mount for cifs / Samba file shares
%nebnews ALL = /bin/mount, /bin/umount
```

Set `nebnews` group as owner of necessary directories

```bash
chgrp -R nebnews /var/local/newspapers
chgrp -R nebnews /var/local/www/django/openoni/log
chgrp -R nebnews /var/local/www/django/openoni/data/word_coordinates
```

### Clone Open ONI

```bash
mkdir /var/local/www/django
chgrp webadmins /var/local/www/django
chmod 2775 /var/local/www/django
cd /var/local/www/django
```

Run these commands as a regular user rather than root

```bash
git clone git@github.com:open-oni/open-oni.git openoni
cd openoni
git checkout main
```

### SELinux Permissions
```bash
# Newspapers data needs to be readable by Apache for PDFs, JP2s, and OCR XML
semanage fcontext -a -t httpd_sys_content_t "/var/local/newspapers(/.*)?"

# Python executables need httpd-executable SELinux context
semanage fcontext -a -t httpd_sys_script_exec_t "/var/local/www/django/openoni/ENV/lib/python3.14/site-packages/.+\.so"

# Static asset path needs Apache write access
mkdir /var/local/www/django/openoni/static/compiled
semanage fcontext -a -t httpd_sys_rw_content_t "/var/local/www/django/openoni/static/compiled(/.*)?"

# Django log files
semanage fcontext -a -t httpd_sys_rw_content_t "/var/local/www/django/openoni/log(/.*)?"
touch log/debug.log
chown apache log/debug.log

# Examine non-standard SELinux file contexts
ll -Z static
ll -Z log
ll -Z ENV/lib/python3.9/site-packages/**/*.so

# IF initial setup before batch files have been copied and ingested
restorecon -F -R /var/local/www/django/openoni

# IF batch files already copied and ingested, we want to ignore them for speed
# Run these commands to set SELinux context on all files but exclude recursing
# into data/batches/ and data/word_coordinates/ directories
cd /var/local/www/django/openoni

shopt -s extglob
restorecon -F -R !('data')
restorecon -F data
restorecon -F data/*
shopt -u extglob
```

### File-based Cache Directory
This is only used if the production settings file is enabled in Open ONI's `settings_local.py`

```bash
mkdir -p /var/tmp/django_cache
chown apache:nebnews /var/tmp/django_cache
chmod 2770 /var/tmp/django_cache
```

### Python Virtual Environment
Run these commands as a regular user rather than root

```bash
cd /var/local/www/django/openoni

# Create and activate Python virtual environment
python3.14 -m venv ENV
source ENV/bin/activate

# Update pip and setuptools
pip install -U pip
pip install -U setuptools

# Install / update Open ONI dependencies
pip install -r requirements.lock
```

### Config files

```bash
cd onisite
cp urls_example.py urls.py
cp settings_local_example.py settings_local.py
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
cd /var/local/www/django/openoni
source ENV/bin/activate
./manage.py setup_index
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

    # Open ONI
    'django.contrib.humanize',  # Added to make data more human-readable
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
mkdir /var/local/www/django/openoni/log/reviewed
chown -R apache:nebnews /var/local/www/django/openoni/log
```

#### URLs
Set the URLs file to use the theme and plugins it incorporates

`vim onisite/urls.py`:
```python
from django.urls import include, path, re_path
from onisite.plugins.featured_content import views as fc_views

urlpatterns = [
  # Plugin URLs
  path('', include("onisite.plugins.calendar.urls")),
  re_path(r'^$', views.featured, name="featured_home"),
  re_path(r'^map', include("onisite.plugins.map.urls")),

  # Theme URLs
  path('', include("themes.nebraska.urls")),

  # Open ONI URLs
  path('', include("core.urls")),
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

./manage.py collectstatic -c
./manage.py collectstatic --noinput

# Grant write access for both Apache and group
sudo chown -R apache static/compiled/
sudo chmod -R g+w static/compiled/
```

In production environments, perform a graceful Apache restart after re-compiling static assets so the app uses the updated static file hash fingerprints in the URLs rendered in templates:

```bash
sudo apachectl graceful
```

## Load Batches

Instructions for loading batches are available in the [README](../README.md).
