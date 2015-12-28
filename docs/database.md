# Setup Postgres

## RHEL7 Pre-setup

```bash
# Postgres 9.4:

sudo rpm -iUvh http://yum.postgresql.org/9.4/redhat/rhel-7-x86_64/pgdg-redhat94-9.4-2.noarch.rpm
sudo yum -y update
sudo yum -y install postgresql94 postgresql94-server postgresql94-contrib postgresql94-libs

# Configure Postgres to start when the server boots:
sudo systemctl enable postgresql-9.4


```

## Setup database

```bash
# Init db
## Ubuntu
sudo postgresql-setup initdb
## RHEL7
sudo /usr/pgsql-9.4/bin/postgresql94-setup initdb

# start service
# Ubunto
sudo service postgresql start
# Redhat
sudo systemctl start postgresql-9.4
```

Edit the following file:

```bash
# Ubuntu:
sudo vi /etc/postgresql/9.3/main/pg_hba.conf
# Redhat:
sudo vi /var/lib/pgsql/9.4/data/pg_hba.conf
```
Replace all *peer* or *ident* at the end by *md5*:

E.g.:
```
# "local" is for Unix domain socket connections only
local   all             all                                     peer
# IPv4 local connections:
host    all             all             127.0.0.1/32            ident
```
by
```
# "local" is for Unix domain socket connections only
local   all             all                                     ident
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
```

Note:
To access the database through the command line (i.e. `psql`) we need to use `ident`.
From django we need `md5`. **Need to confirm this!**.

Restart postgres:
```
# Ubuntu
sudo service postgresql restart
# Redhat
sudo systemctl restart postgresql-9.4

```

# Test:
```

sudo su - postgres
psql

```

## Create database

Configure Postgres:  
```bash
# Enter as postgres user
sudo su - postgres

# Database and username/password is available in the ```.env``` file
# that should have been provided separately.

# Create user reduction
#
createuser -P -s -e reduction

# Once postgres user, create a db
createdb -O reduction -W reduction
```
## Test

Test the database. This should work:
*Note*:
To use user/pass the settings above must be in *md5*!
```
psql --username=reduction -W reduction
# list all databases
\list
# Connect to database:
\connect reduction
# list all tables in the current database
\dt
```

## Usefull


Delete all tables owened by a user:
```
drop owned by reduction;
```
