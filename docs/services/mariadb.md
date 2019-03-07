# MariaDB

**Contents**

- [Install](#install)
- [Access Control](#access-control)
- [Backups](#backups)


## Install

Install documentation is located in the private CDRH-General repo

Follow the instructions on this wiki page:
- [MariaDB](https://github.com/CDRH/CDRH-General/wiki/MariaDB)

Django also requires development libraries from MariaDB

`yum install mariadb-devel`


## Access Control

Create schema `openoni`

Add `openoni` user only connecting from `localhost`

Grant `openoni` user all privileges except `GRANT OPTION`
on `openoni%` schema(s)


## Backups
Our backup script is located in the private servers repo

[MariaDB Backup Script](https://github.com/CDRH/servers/blob/master/mariadb/backup/dump_dbs.sh)

Download this script to `/var/local/mariadb/backup/`

Running the script will instruct that it must be run as `root` and one must add
the root MariaDB password to `/root/.my.cnf` like

```ini
[mysql]
password=abc

[mysqldump]
password=abc
```

As the file contains a sensitive password,
ensure `/root/.my.cnf` is only readable by `root`

Schedule a regular backup in `/etc/crontab`:
```cron
# REGULAR TASKS

# Daily MariaDB Backup at 2am
  0  2  *  *  * root       /var/local/mariadb/backup/dump_dbs.sh -qs
```

