from os import urandom
from fabric.api import cd, env, put,  run, sudo, task, local

project_name = '{{ cookiecutter.repo_name }}'
env.hosts = ['root@{{ cookiecutter.repo_name }}.se']

venv = 'source /var/www/venv/site/bin/activate'
site_root = '/var/www/%s/' % project_name
git_repo = '{{ cookiecutter.repo_name }}'
db_password = urandom(16).encode('hex')
secret_key = urandom(32).encode('hex')

@task
def setup():
    """
    Setup a fresh virtualenv as well as a few useful directories, then run
    a full deployment
    """

    sudo('yes | apt-get install postgresql postgresql-server-dev-9.1')

    sudo('psql -c "CREATE USER django WITH NOCREATEDB NOCREATEUSER ENCRYPTED PASSWORD E\'%s\'"' % db_password, user='postgres')
    sudo('psql -c "CREATE DATABASE %s WITH OWNER django"' % project_name, user='postgres')
    
    sudo('yes | apt-get install python-setuptools libpython-dev python-dev git')
    sudo('easy_install pip')
    sudo('pip install virtualenv')
    sudo('yes | apt-get install nginx')
    sudo('yes | apt-get install uwsgi uwsgi-plugin-python')
    sudo('yes | apt-get install libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev')

    sudo('mkdir /var/www')
    sudo('chown -R root /var/www/')
    run('mkdir /var/www/venv')
    run('cd /var/www/venv; virtualenv site')

    sudo('echo "export DATABASE_URL=postgres://django:%s@localhost:5432/%s" >> /var/www/venv/site/bin/activate' % (db_password, project_name))
    sudo('echo "export SECRET_KEY=\'%s\'" >> /var/www/venv/site/bin/activate' % secret_key)
    sudo('echo "export DJANGO_SETTINGS_MODULE=%s.settings.production" >> /var/www/venv/site/bin/activate' % project_name)
    run('cd /var/www; git clone %s' % git_repo)
    
    put('config/nginx/%s' % project_name, '/etc/nginx/sites-available/%s' % project_name, use_sudo=True)
    sudo('ln -s /etc/nginx/sites-available/%s /etc/nginx/sites-enabled/%s' % (project_name, project_name))
    sudo('rm /etc/nginx/sites-enabled/default')

    put('config/uwsgi/%s.ini' % project_name, '/etc/uwsgi/apps-available/%s.ini' % project_name, use_sudo=True)
    sudo('echo "\nenv = DATABASE_URL=postgres://django:%s@localhost:5432/%s" >> /etc/uwsgi/apps-available/%s.ini' % (db_password, project_name, project_name))
    sudo('echo "env = SECRET_KEY=\'%s\'" >> /etc/uwsgi/apps-available/%s.ini' % (secret_key, project_name))
    sudo('ln -s /etc/uwsgi/apps-available/%s.ini /etc/uwsgi/apps-enabled' % project_name)

    sudo('chown -R www-data /var/www/')

    deploy_migrate_and_static()

@task(alias="d")
def basic_deploy():
    with cd(site_root):
        _get_code()
        _install_deps()
        _reload()

@task(alias="dm")
def deploy():
    with cd(site_root):
        _get_code()
        _install_deps()
        _migrate()
        _reload()

@task(alias="dms")
def deploy_migrate_and_static():
    with cd(site_root):
        _get_code()
        _install_deps()
        _migrate()
        _collectstatic()
        _reload()

@task(alias="ds")
def deploy_static():
    with cd(site_root):
        _get_code()
        _install_deps()
        _collectstatic()
        _reload()

@task(alias="r")
def reload():
    with cd(site_root):
        _reload()

def _install_deps():
    sudo("%s && pip install -r requirements.txt" % venv)


def _migrate():
    run("%s && python manage.py syncdb" % venv)
    run("%s && python manage.py migrate" % venv)


def _collectstatic():
    run("%s && python manage.py collectstatic -v0 --noinput" % venv)


def _get_code():
    run("git pull origin master")


def _reload():
    run("touch reload")

@task(alias='mpl')
def mirror_production_to_local():
    sudo('pg_dump %s -f /tmp/database.txt' % project_name, user='postgres')
    local('scp %s:/tmp/database.txt /tmp' % env.hosts[0])
    local('sudo su postgres -c \"dropdb %s\"' % project_name)
    local('sudo su postgres -c \"createdb %s\"' % project_name)
    local('sudo su postgres -c \"psql -d %s -f /tmp/database.txt\"' % project_name)
    local('scp -r %s:%s%s/media/uploads/ ./%s/media/' % (env.hosts[0], site_root, project_name, project_name))