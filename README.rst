about
=====
Runs your Django management commands via cron and gives you some success and
log infos in admin.

features
--------
* Single entry in crontab that forks new processes for scheduled commands
* Define which management command when to run via django admin
* Logs success state, stdout and stderr into database log

setup
=====
Install via pip::

    pip install django-command-scheduler

Add to `INSTALLED_APPS`::

    INSTALLED_APPS = (
        ...
        'command_scheduler',
    )

Run `migrate`::

    python manage.py migrate

Insert command a single line into crontab::

    * * * * * /path/to/possibly/virtualenv/bin/python /path/to/manage.py runcommands

Now go to admin site and add commands!

todos
=====
* Tests (!)
* Notentifications on error

license
=======
MIT-License, see LICENSE file.
