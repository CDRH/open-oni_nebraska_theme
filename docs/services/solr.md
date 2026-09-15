# Solr 9.x

## Install

Install documentation is located in the private servers repo

Follow the instructions on this wiki page:
- [Solr](https://github.com/CDRH/servers/blob/el9/docs/Solr.md)

## Create Open ONI Core
```bash
sudo -u solr /opt/solr/bin/solr create_core -c openoni
```

## Backups
Our backup scripts are located in the private servers repo

[Solr Scripts](https://github.com/CDRH/servers/tree/el9/solr)

Follow the instructions in the accompanying README.md file.

Copy default settings file. Edit if desired, but not needed.

```bash
cd /var/local/cdrh-servers/solr/backup
cp settings_example.py settings.py
```

Schedule a regular backup in `/etc/crontab`:
```cron
# REGULAR TASKS

# Daily Solr Backup at 4am
  0  3  *  *  * solr       /var/local/cdrh-servers/solr/backup/backup.py -q
```

## Configure
Further config is handled after the Open ONI repository is cloned

[Configure Open ONI Schema](/docs/openoni.md#solr-schema)
