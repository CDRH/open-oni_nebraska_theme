# Solr 6.x

**Contents**

- [Install](#install)
- [Create OpenONI Core](#create-openoni-core)
- [Backups](#backups)
- [Configure](#configure)


## Install

Install documentation is located in the private CDRH-General repo

Follow the instructions on this wiki page:
- [Solr](https://github.com/CDRH/CDRH-General/wiki/Solr)


## Create OpenONI Core
```bash
sudo -u solr /opt/solr/bin/solr create_core -c openoni
```


## Backups
Our backup scripts are located in the private servers repo

[Solr Scripts](https://github.com/CDRH/servers/tree/master/solr)

Download the files to `/var/local/solr/`

Follow the instructions in the accompanying README.md file

Schedule a regular backup in `/etc/crontab`:
```cron
# REGULAR TASKS

# Daily Solr Backup at 4am
  0  4  *  *  * solr       /var/local/solr/backup/backup.py -q
```


## Configure
Further config is handled after the OpenONI repository is cloned

[Configure OpenONI Schema](/docs/openoni.md#solr-schema)

