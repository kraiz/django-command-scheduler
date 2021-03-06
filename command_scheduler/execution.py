import signal
import sys
import os

from io import StringIO
from contextlib import contextmanager

from django.core.management import execute_from_command_line
from django.utils.timezone import now

from command_scheduler.models import Command, Log


def signal_term_handler(signal, frame):
    raise RuntimeError('Command aborted')


@contextmanager
def redirected(out=sys.stdout, err=sys.stderr):
    sys.stdout, sys.stderr = out, err
    try:
        yield
    finally:  # recover
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


def execute_command(command_pk):
    signal.signal(signal.SIGTERM, signal_term_handler)

    command = Command.objects.get(pk=command_pk)

    # prevent parallel execution if enabled
    if not command.parallel:
        if command.last_log is not None and command.last_log.is_running():
            return  # old instance still running

    log = Log.objects.create(command=command, pid=os.getpid())

    if command.save_output:
        stdout = StringIO()
        stderr = StringIO()
    else:
        stdout = sys.stdout
        stderr = sys.stderr

    try:
        with redirected(out=stdout, err=stderr):
            execute_from_command_line(
                ['manage.py', command.name] + command.params.split()
            )
    except:
        import traceback

        stderr.write(traceback.format_exc())
        success = False
    else:
        success = True
    finally:
        log.success = success
        log.ended = now()
        if command.save_output:
            log.stdout = stdout.getvalue()
            log.stderr = stderr.getvalue()
        log.save()
