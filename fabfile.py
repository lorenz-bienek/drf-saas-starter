import os

from fabric.api import env, lcd, local, task


def _relative_to_fabfile(*path):
    return os.path.join(os.path.dirname(env.real_fabfile), *path)


@task
def clean():
    """Remove all generated files (.pyc, .coverage, .egg, etc)."""
    with lcd(_relative_to_fabfile()):
        local('find . -name "*.pyc" -exec rm -rf {} \;')
        local('find . -name ".coverage" -exec rm -rf {} \;')
        local('find . -name ".DS_Store" -exec rm -rf {} \;')
        local('find . -name "._DS_Store" -exec rm -rf {} \;')
        local('find . -name "._*.*" -exec rm -rf {} \;')
        local('rm -f .coverage.*')
        local('rm -rf build')
        local('rm -rf dist')


@task
def flake8():
    """Use flake8 to check Python style, PEP8, and McCabe complexity.
    See http://pypi.python.org/pypi/flake8/
    .. note::
        * Files with the following header are skipped::
            # flake8: noqa
        * Lines that end with a ``# NOQA`` comment will not issue a warning.
    """

    local('flake8 --statistics --exit-zero')


@task
def isort():
    """Use isort to automatically (re-)order the import statements on the top of files."""
    with lcd(_relative_to_fabfile()):
        local('isort -rc .')


@task
def build():
    """Prepare the code to be commited."""
    clean()
    isort()
    flake8()
    test()


@task
def test():
    local('py.test')


@task
def commit(message):
    """Git Commit with a message."""
    build()
    local('git add .')
    local('git commit -m "%s"' % message)


@task
def push():
    """Push to Git."""
    local('git push')


@task
def commit_and_push(message):
    """Commit and push in once."""
    build()
    commit(message)
    push()


@task
def coverage():
    """Run coverage."""
    local('coverage py.test')
    local('coverage html')


@task
def update():
    """Local setup for a new developer."""

    if "VIRTUAL_ENV" not in os.environ:
        print("No virtual env found - please run:")
        print("$ ./local_setup.py {{ project_name }}")
        print("$ source .venv/bin/activate")

    local('pip install -r requirements/local.txt')
    local('python manage.py migrate')


@task
def pull_and_update(branch="master"):
    local("git checkout %s" % branch)
    local("git pull %s" % branch)
    update()


@task
def push_to_heroku():
    local("git push heroku master")
    local('heroku run "python manage.py migrate" --app drf-saas-starter')


@task
def create_heroku_app(app_name):

    local('heroku create %s --buildpack https://github.com/heroku/heroku-buildpack-python  --region eu' % app_name)

    # Attach addons from einhorn-default
    local('heroku addons:attach cloudamqp-opaque-72597 --app %s' % app_name)
    local('heroku addons:attach postgresql-acute-80214 --app %s' % app_name)
    local('heroku addons:attach redis-octagonal-12968 --app %s' % app_name)
    local('heroku addons:attach librato-flat-96442 --app %s' % app_name)

    # Enabling the labs
    local('heroku labs:enable log-runtime-metrics --app %s' % app_name)
    local('heroku labs:enable runtime-dyno-metadata --app %s' % app_name)

    # Setting up backups
    local('heroku pg:backups schedule DATABASE_URL --at "02:00 UTC" --app %s' % app_name)

    # Setting up config
    local('heroku config:set ADMIN_URL="$(openssl rand -base64 32)" '
          'PYTHONHASHSEED=random '
          'SECRET_KEY="$(openssl rand -base64 64)" '
          'ALLOWED_HOSTS=%s.herokuapp.com --app %s' % (app_name, app_name))

    local('heroku git:remote --app %s' % app_name)

    # local('heroku config:set SENTRY_DSN=%s --app %s' % (os.getenv('SENTRY_DSN'), app_name))
    #
    # local('heroku run python manage.py createsuperuser --app %s' % app_name)


@task
def licenses():
    """Update the licenses of all installed pip packages."""
    local("echo '# Licenses' > docs/licenses.md")
    local("echo '' >> docs/licenses.md")
    local("echo 'A list of the used packages and their licenses (can be updated with the command 'fab licenses') > docs/licenses.md' >> docs/licenses.md")
    local("echo '' >> docs/licenses.md")
    local("yolk -l -f license >> docs/licenses.md")


@task
def pip(update="none"):
    """Update the pip requirements."""

    print("DEPRECATED, use make pip-compile, make pip-update or make pip-install")
