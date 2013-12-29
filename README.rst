about
=====
Runs your Django management commands via crontab or onclick in admin site and
gives you some success and log infos.

features
--------
* Single entry in crontab that forks new processes for scheduled commands
* Define which management command to run when via Django admin
* Logs success state, stdout & stderr into database log

setup
=====
Install via pip::

    pip install django-command-scheduler

Add to `INSTALLED_APPS`::

    INSTALLED_APPS = (
        ...
        'command_scheduler',
    )

Run `syncdb`::

    python manage.py syncdb

Insert command a single line into crontab::

    * * * * * /path/to/possibly/virtualenv/bin/python /path/to/manage.py runcommands

Now go to admin site and add commands!

todo
====
* Python 3 support
* Notentifications on error

license
=======
MIT-License, see LICENSE file.
