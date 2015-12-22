# Production

## Clone:
```
shh -X reduction.sns.gov
cd git
git clone git@github.com:ricleal/DjangoAdminLTE.git
cd DjangoAdminLTE
```

## Folders

Create necessary folders and clone projects:

```
mkdir contrib
cd contrib
git clone  git@github.com:almasaeed2010/AdminLTE.git
git clone git@github.com:twbs/bootstrap.git
```

## Virtual environment

```
virtualenv env
source env/bin/activate
pip install -r config/requirements/production.txt
```

## Configuration

Create file:
```
vi ./config/settings/.env
# Put inside
SETTINGS_MODULE=config.settings.production
DEBUG=False
SECRET_KEY='XXXXXX'
DATABASE_URL=postgres://reduction:XXXX@localhost:5432/XXXXX
ADMIN_URL="r'^XXXXX/'"
```

## Database

Since the user ```reduction``` already exists, let's just add the database:

```
# Make sure postgresql is running:
sudo service postgresql status

# Enter as postgres user
sudo su - postgres

# Once postgres, create a db
createdb -O <owner>  -U <user> -W <db name>
createdb -O reduction  -U reduction -W XXXX

# Test it:
psql --username=reduction -W XXXX

# list all tables
\dt
# list all databases
\list

```

## Deploy:

```
# Must be identical to: config/settings/production.py
# STATIC_ROOT = '/var/nginx/reduction_service/new/static'
DEST=/var/www/reduction_service/DjangoAdminLTE
sudo mkdir $DEST

# Must be the same as in: config/settings/production.py
# STATIC_ROOT = '/var/nginx/reduction_service/DjangoAdminLTE/static'
sudo mkdir $DEST/static

sudo cp -r DjangoAdminLTE/* $DEST/
sudo chmod -R 0755 $DEST

cd $DEST
sudo -S

# If you coppied env, delete it
rm -f env
virtualenv env
source env/bin/activate

source env/bin/activate
./env/bin/pip install -r config/requirements/production.txt

# Set env variable
export DJANGO_SETTINGS_MODULE="config.settings.production"

./env/bin/python manage.py collectstatic --noinput
./env/bin/python manage.py makemigrations
./env/bin/python manage.py migrate

```
