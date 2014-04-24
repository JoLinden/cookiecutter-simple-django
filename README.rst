cookiecutter-simple-django
==========================

A cookiecutter_ template for Django.

.. _cookiecutter: https://github.com/audreyr/cookiecutter

Usage
------

Let's pretend you want to create a Django project called "redditclone". Rather than using `startproject`
and then editing the results to include your name, email, and various configuration issues that always get forgotten until the worst possible moment, get cookiecutter_ to do all the work.

First, get cookiecutter. Trust me, it's awesome::

Set up your virtualenv::

    $ cd <your-envs-folder>
    $ virtualenv  --no-site-packages redditclone
    $ cd redditclone
    $ source bin/activate
    $ pip install cookiecutter

Now run it against this repo::

    $ cd <your-workspace>
    $ cookiecutter  https://github.com/JoLinden/cookiecutter-simple-django.git


Structure
---------

The structure used should look quite familiar:

**Requirements**

The ``requirements`` folder contains a requirements file for each environment.

If you need to add a dependency please choose the right file.

**Settings**

The ``settings`` folder contains a settings file for each environment and the ``local`` settings should be gitignored.

If you take a look at ``base.py``, you'll see that it includes the optional module ``local.py``
in the same folder. There you can override the local values and gitignore will
exclude it from your commits.

The ``testing.py`` module is loaded automatically after ``base.py`` and ``local.py`` every time you
run ``python ./manage.py test``.

**Apps**

The ``apps`` folder should contain all your local django apps, this is to keep
the structure of the project clean.

When it's time to ``python ./manage.py startapp <name>``, just move the generated
module to ``apps``. If you want to know why this works, just take a look at the line::

    sys.path.insert(0, root('apps'))

in ``settings/base.py``.