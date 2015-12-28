# Web server

## RHEL7 Pre-setup

```
sudo yum install nginx uwsgi
sudo yum install python-pip
sudo yum install python-virtualenv
```

## Try the uWSGI first!

Note:
It needs to be in development or production mode!!!
If not done yet, do:
```
source env/bin/activate
./env/bin/pip install -r ./config/requirements/production.txt

```

```
# Set settings to local
export DJANGO_SETTINGS_MODULE="config.settings.local"

# Collect static files in the static folder:
python manage.py collectstatic

# Test with the static
./env/bin/uwsgi --http :8001 --module config.wsgi --static-map /static=static
```

Open a browser: `http://localhost:8001/`.

## Start the service:

``` bash
# Configure Postgres to start when the server boots:
# Ubuntu
sudo service nginx start
# redHat
sudo systemctl start nginx
sudo systemctl enable nginx # enable at startup

```

# TODO: check steps below!!

## Deployment no SSL

Copy everything for now:
```
cd /var/nginx/reduction_service
sudo cp -r ~/git/reduction_service/* .
```

Enable the configuration:
```
sudo ln -s /var/nginx/reduction_service/nginx/reduction_local_nginx.conf  /etc/nginx/sites-enabled/
```

```
sudo /etc/init.d/nginx restart
```

Start the uwsgi server. It uses a socket to communicate with nginx
```
cd /var/nginx/reduction_service
sudo uwsgi --socket reduction.sock --module config.wsgi --chmod-socket=666
# or
sudo uwsgi --ini nginx/reduction_uwsgi.ini
```

## Deployment SSL

Create key and certificate if needed:
```
cd ssl/
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout reduction.key -out reduction.crt
```

Enable the configuration:
```
sudo rm default
sudo rm /var/nginx/reduction_service/nginx/reduction_local_nginx.conf
sudo ln -s /var/nginx/reduction_service/nginx/reduction_dev_nginx.conf  /etc/nginx/sites-enabled/
sudo /etc/init.d/nginx restart
sudo uwsgi --ini nginx/reduction_uwsgi.ini
```

# RHEL 7


## Disable Apache

```
# Disable Apache
sudo service httpd status
sudo systemctl disable httpd.service
sudo service httpd status
sudo systemctl stop httpd.service
```

## Add new software
```
# install
sudo yum install nginx
sudo pip install uwsgi
```

## Start nginx

```
sudo service nginx status
sudo service nginx start

```
Test: http://reduction.sns.gov/

## Deployment

```
rm -rf /SNS/users/rhf/git/reduction_service/env
cd /SNS/users/rhf/git/reduction_service/
cp env_prod config/settings/.env
virtualenv env
source env/bin/activate
pip install -r requirements/production.txt
```

Copy everything for now:
```
sudo mkdir -p  /var/nginx/reduction_service
cd /var/nginx/reduction_service
sudo cp -r /SNS/users/rhf/git/reduction_service/* .
```
Only in redhat:
```
# If the folders don't exist!
sudo mkdir /etc/nginx/sites-available
sudo mkdir /etc/nginx/sites-enabled
# vi /etc/nginx/nginx.conf
# add inside the http block: include /etc/nginx/sites-enabled/*;
```

Enable the configuration:
```

sudo ln -s /var/nginx/reduction_service/nginx/reduction_prod_nginx.conf  /etc/nginx/sites-enabled/
sudo service nginx restart

nohup sudo -E uwsgi --ini nginx/reduction_uwsgi.ini &
```

## Open ports if needed (REHL7)

```
sudo firewall-cmd  --zone=public --add-port=80/tcp --permanent
sudo firewall-cmd  --zone=public --add-port=443/tcp --permanent
sudo firewall-cmd  --reload

```
