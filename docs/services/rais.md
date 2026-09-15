# RAIS

## Install

### Dependencies

```bash
dnf install gcc openjpeg2-devel pkgconf-pkg-config
```

### Install go

As regular user

```bash
cd /var/local
wget https://go.dev/dl/go1.24.2.linux-amd64.tar.gz
tar -C /usr/local/share -xzf go1.24.2.linux-amd64.tar.gz

ln -s /usr/local/share/go/bin/* /usr/local/bin/
ln -s /usr/local/share/go/bin/* /usr/local/sbin/

# Set gopath as `/var/local/go` due to more storage required for packages etc
echo 'export GOPATH=/var/local/go' > /etc/profile.d/z-gopath.sh
mkdir /var/local/go
chgrp webadmins /var/local/go
chmod 2775 /var/local/go
```

### Clone from GitHub

```bash
git clone https://github.com/uoregon-libraries/rais-image-server /usr/local/share/rais

cd /usr/local/share/rais

# Checkout latest release tag
git checkout v4.2.4

make rais-server
```

### Configuration File

```bash
cp rais-example.toml /etc/rais.toml
vim /etc/rais.toml
```

```toml
LogLevel = "WARN"

TilePath = "/var/local/newspapers"

IIIFWebPath = "/rais"

IIIFBaseURL = "https://(ServerName)"

CapabilitiesFile = "/usr/local/share/rais/cap-max.toml"
```

### Systemd Service

```bash
# Create user and group for rais
useradd -M rais
```

`vim /etc/systemd/system/rais.service`

```ini
[Unit]
Description=RAIS image server
Documentation=https://github.com/uoregon-libraries/rais-image-server/wiki
After=network.target httpd.service
Wants=httpd.service

[Install]
WantedBy=multi-user.target

[Service]
Type=simple
User=rais
Group=rais

ExecStart=/usr/local/share/rais/bin/rais-server

KillSignal=SIGTERM
# Don't want to see an automated SIGKILL ever
SendSIGKILL=no

SyslogIdentifier=rais
SyslogLevel=warning

Restart=always
RestartSec=150

UMask=007

# Reasonable time for the server to start up/shut down
TimeoutSec=60

# Place temp files in a secure directory, not /tmp
PrivateTmp=true
```

```bash
systemctl enable rais
systemctl start rais
```

If execution errors on the service start despite permissions and ownerships
looking correct, the files may need SELinux context reset:

```bash
restorecon -R -F /usr/local/share/rais
```

### SELinux Port Permission

```bash
#semanage port -a -t http_port_t -p tcp 12415
```

### Add Apache Config
Copy [RAIS Apache config](/conf/apache/rais.conf) into the drop-in directory which will be included in your virtual host block

```bash
cp /var/local/www/django/openoni/themes/nebraska/conf/apache/rais.conf /etc/httpd/local/vhosts/_(ServerName).unl.edu/
```
