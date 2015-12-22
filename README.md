# Start

## Assumptions

- Local : no webserber. Django is run through the command: ```./manage runserver```.
- Development: Same code running on a webserver. Usually this runs on Ubuntu.
- Production: Production code. This Runs on RHEL7 with proper signed SSL certificates.

An enviroment variable named ```DJANGO_SETTINGS_MODULE``` must be defined.

This variable is called by either:
- [manage.py](manage.py)
- [config/wsgi.py](config/wsgi.py)

In the [manage.py](manage.py) the ```DJANGO_SETTINGS_MODULE``` is predefined with settings for local [config.settings.local](config/settings/local.py).

In the [config/wsgi.py](config/wsgi.py) the ```DJANGO_SETTINGS_MODULE```is predefined with settings for production [config.settings.production](config/settings/production.py).

Usually both [local](config/settings/local.py) and [production](config/settings/production.py) don't need to be changed.
There is an [.env](config/settings/.env) file that you should have been provided with the respective environment configurations.

An example for production is:
```
DEBUG=False
SECRET_KEY=<your secret key>
DATABASE_URL=postgres://<user>:<pass>@localhost:5432/<db name>
ADMIN_URL="r'^<admin interface folder>/'"
ALLOWED_HOSTS=localhost,127.0.0.1,<etc...>
```
This file must saved as ```config/settings/.env```.

## Database Configuration

See [docs/database.md](docs/database.md).

## Setup the the virtual environment:
```
virtualenv env
source env/bin/activate
pip install -r config/requirements/local.txt
```

## Run server:

```
./manage.py makemigrations
```
```
Migrations for 'admin':
  0001_initial.py:
    - Create model LogEntry
Migrations for 'contenttypes':
  0001_initial.py:
    - Create model ContentType
    - Alter unique_together for contenttype (1 constraint(s))
Migrations for 'auth':
  0001_initial.py:
    - Create model User
    - Create model Group
    - Create model Permission
    - Add field permissions to group
    - Add field groups to user
    - Add field user_permissions to user
    - Alter unique_together for permission (1 constraint(s))
Migrations for 'sessions':
  0001_initial.py:
    - Create model Session
```

```
./manage.py migrate
```
```
Operations to perform:
  Apply all migrations: admin, contenttypes, auth, sessions
Running migrations:
  Rendering model states... DONE
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying sessions.0001_initial... OK
```

```
./manage.py runserver
```
### Folders

- env

Where the virstula environment is created


- contrib

Clone of projects:

AdminLTE:
https://github.com/almasaeed2010/AdminLTE

```
git clone  git@github.com:almasaeed2010/AdminLTE.git
```
bootstrap:
https://github.com/twbs/bootstrap

```
git clone git@github.com:twbs/bootstrap.git
```

- static has links to:

AdminLTE -> ../contrib/AdminLTE/dist/
AdminLTE_plugins -> ../contrib/AdminLTE/plugins/
bootstrap -> ../contrib/bootstrap/dist/
