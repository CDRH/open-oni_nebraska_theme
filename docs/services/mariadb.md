# MariaDB

## Install

Install documentation is located in the private servers repo

Follow the instructions on this wiki page:
- [MariaDB](https://github.com/CDRH/servers/blob/el9/docs/MariaDB.md)

Django also requires development libraries from MariaDB

`dnf install mariadb-devel`

## Access Control

`sudo mysql`:

```sql
CREATE DATABASE openoni;

CREATE USER 'openoni'@'localhost' IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES ON `openoni`.* TO 'openoni'@'localhost';

SHOW GRANTS FOR 'openoni'@'localhost';
```

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

