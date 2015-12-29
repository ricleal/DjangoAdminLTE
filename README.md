# New Reduction server

Based on: [AdminLTE Control Panel Template](https://almsaeedstudio.com/).


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

## Run Django embebed server (only for local testing/development!):

```
./manage.py makemigrations
./manage.py migrate
./manage.py runserver
```

## Folders

Explanation of the folders:

**`env`**:

Where the virtual environment is created

**`contrib`**:

Clone of projects:

AdminLTE:
https://github.com/almasaeed2010/AdminLTE

```
git clone git@github.com:almasaeed2010/AdminLTE.git
# or
git clone https://github.com/almasaeed2010/AdminLTE.git
```

Bootstrap:
https://github.com/twbs/bootstrap

```
git clone git@github.com:twbs/bootstrap.git
# or
git clone https://github.com/twbs/bootstrap.git
```

Note that `server/static` has links to the `contrib` folder:
```
AdminLTE -> ../contrib/AdminLTE/dist/
AdminLTE_plugins -> ../contrib/AdminLTE/plugins/
bootstrap -> ../contrib/bootstrap/dist/
```

## Web Server (Mainly Production)

NGINX : Only for production or Development!

uWSGI: Standalone for Development and will communicate with NGINX for production.

See [docs/nginx.md](docs/nginx.md).

TODO: Not finished yet!

## TODO: Deployment script!
