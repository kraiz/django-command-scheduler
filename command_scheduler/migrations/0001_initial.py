# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import command_scheduler.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, choices=[])),
                ('params', models.CharField(max_length=255, blank=True)),
                ('time', models.CharField(validators=[command_scheduler.models.cron_validator], help_text='Cron expresion (min, hour, day of month, month, day of week)', max_length=255)),
                ('enabled', models.BooleanField(default=True)),
                ('save_output', models.BooleanField(default=True, help_text='Save output of command into the log entry')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('started', models.DateTimeField(auto_now_add=True)),
                ('ended', models.DateTimeField(blank=True, null=True)),
                ('pid', models.IntegerField()),
                ('stdout', models.TextField(blank=True)),
                ('stderr', models.TextField(blank=True)),
                ('success', models.NullBooleanField(default=None)),
                ('command', models.ForeignKey(related_name='logs', to='command_scheduler.Command')),
            ],
        ),
    ]
