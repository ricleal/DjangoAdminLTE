# Start

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

bootstrap:
https://github.com/twbs/bootstrap

- static has links to:

AdminLTE -> ../contrib/AdminLTE/dist/
AdminLTE_plugins -> ../contrib/AdminLTE/plugins/
bootstrap -> ../contrib/bootstrap/dist/
