# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('command_scheduler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='parallel',
            field=models.BooleanField(default=False, help_text='Allow parallel execution?'),
        ),
    ]
