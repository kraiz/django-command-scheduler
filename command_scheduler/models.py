from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from croniter import croniter
from command_scheduler.util import build_command_choices
from datetime import datetime
import os
import errno
import signal


def cron_validator(value):
    try:
        croniter(value)
    except KeyError as ke:
        raise ValidationError('Invalid value: ' + ke.message)
    except ValueError as ve:
        raise ValidationError(ve.message)


class Command(models.Model):
    name = models.CharField(max_length=255, choices=build_command_choices())
    params = models.CharField(max_length=255, blank=True)
    time = models.CharField(
        max_length=255,
        validators=[cron_validator],
        help_text='Cron expresion (min, hour, day of month, month, day of week)'
    )

    enabled = models.BooleanField(default=True)
    save_output = models.BooleanField(
        default=True,
        help_text='Save output of command into the log entry'
    )

    def __unicode__(self):
        return self.name

    @property
    def next_execution(self):
        if self.enabled:
            return croniter(self.time, now()).get_next(datetime)
        else:
            return None

    @property
    def last_execution(self):
        last_log = self.last_log
        return last_log.started if last_log is not None else None

    @property
    def last_log(self):
        try:
            return self.logs.all().order_by('-started')[0]
        except IndexError:
            return None

    def is_running(self):
        last_log = self.last_log
        return last_log.is_running() if last_log is not None else False


class Log(models.Model):
    command = models.ForeignKey(Command, related_name='logs')
    started = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField(blank=True, null=True)
    pid = models.IntegerField()
    stdout = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    success = models.NullBooleanField(default=None)

    def is_running(self):
        return self._send_signal(0)

    def kill(self):
        killed = self._send_signal(signal.SIGTERM)
        if killed:
            self.success = False
            self.ended = now()
            self.save()
        return killed

    def _send_signal(self, sig):
        try:
            os.kill(self.pid, sig)
        except OSError as e:
            return e.errno == errno.EPERM
        else:
            return True