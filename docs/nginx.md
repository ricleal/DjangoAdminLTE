# Web server

## RHEL7 Pre-setup

```
sudo yum install nginx uwsgi
sudo yum install python-pip
sudo yum install python-virtualenv
```

## start the service:

``` bash
# Configure Postgres to start when the server boots:
# Ubuntu
sudo service nginx start
# redHat
sudo systemctl start nginx
sudo systemctl enable nginx # enable at startup


```
