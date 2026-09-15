# Apache

## Install

Install documentation is located in the private servers repo

[Apache](https://github.com/CDRH/servers/blob/el9/docs/Apache.md)

## Extra Dependencies
Install the latest mod_wsgi from PyPi:
https://modwsgi.readthedocs.io/en/develop/user-guides/installation-from-pypi.html

```bash
source ENV/bin/activate
pip install mod_wsgi
mod_wsgi-express module-config

#LoadModule wsgi_module /var/local/www/django/openoni/ENV/lib/python3.14/site-packages/mod_wsgi/server/mod_wsgi-py314.cpython-314-x86_64-linux-gnu.so

# Update Apache config
cd /etc/httpd/conf.modules.d

# If the dnf package for mod_wsgi was installed, create a `disabled` directory
# and copy the older mod_wsgi module config there
mkdir disabled
cp 10-wsgi-python3.conf disabled/

# Rename or create the module config file
# and populate with the output from mod_wsgi-express module-config above
mv 10-wsgi-python3.conf 10-wsgi-python3.14.conf
vim 10-wsgi-python3.14.conf
```

```apacheconf
<IfModule !wsgi_module>
  LoadModule wsgi_module /var/local/www/django/openoni/ENV/lib64/python3.14/site-packages/mod_wsgi/server/mod_wsgi-py314.cpython-314-x86_64-linux-gnu.so
</IfModule>
```

## Configure

### Directory Indices
Open ONI uses directory indices to allow visitors to browse data files

We generally disable directory indices and the icons the Apache-generated pages
use, so we need to re-enable access to the icons

`vim /etc/httpd/conf.d/autoindex.conf`:

```apacheconf
Alias /icons/ "/usr/share/httpd/icons/"
```

### mod_wsgi Run Directory
Manually create initially:<br>
`mkdir /run/mod_wsgi`

Create automatically at boot going forward

`vim /etc/tmpfiles.d/mod_wsgi.conf`:

```ini
d /run/mod_wsgi 755 root root
```

### Python Randomized Hashing
[Denial-of-Service Protection](https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/#python-options)

No longer needed as this is default behavior since Python 3.3

<del>
`systemctl edit httpd`:
```ini
[Service]
Environment=PYTHONHASHSEED=random
```

`sudo systemctl restart httpd`
</del>

### Virtual Host Config
Copy [Django Apache config](/conf/apache/django.conf) into the drop-in directory which will be included in your virtual host block

```bash
cp /var/local/www/django/openoni/themes/nebraska/conf/apache/django.conf /etc/httpd/local/vhosts/_nebnewspapers*.unl.edu/
```
