"""
Deployment of your django project.
"""

from fabric.api import *

env.hosts = ['lealpc.ornl.gov']
env.user = "root"

INSTALL_DIR = '/var/nginx/reduction_service'


def first_time():
    with cd(INSTALL_DIR):
        virtualenv envvirtualenv env
        source env/bin/activate
./env/bin/pip install -r ./config/requirements/production.txt
sudo cp $HOME/git/DjangoAdminLTE/config/settings/.env /var/nginx/reduction_service/config/settings
export DJANGO_SETTINGS_MODULE="config.settings.production"
sudo -E ./manage.py makemigrations
sudo -E ./manage.py migrate
sudo python manage.py collectstatic --noinput
mkdir contrib
git clone https://github.com/almasaeed2010/AdminLTE.git
git clone https://github.com/twbs/bootstrap.git
cd ..


def update_django_project():
    """ Updates the remote django project.
    """
    with cd(INSTALL_DIR):
        run('git pull')

        with prefix('source %s/env/bin/activate'%INSTALL_DIR):
            run('pip install -r your_pip_requirement_file.txt')
            run('python manage.py syncdb')
            run('python manage.py migrate') # if you use south
            run('python manage.py collectstatic --noinput')

def restart_webserver():
    """ Restarts remote nginx and uwsgi.
    """
    sudo("service uwsgi restart")
    sudo("/etc/init.d/nginx restart")

def deploy():
    """ Deploy Django Project.
    """
    update_django_project()
    restart_webserver()
