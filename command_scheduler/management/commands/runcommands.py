from datetime import datetime, timedelta
from multiprocessing import Process

from django.core.management import BaseCommand
from django.db import connection
from django.utils.timezone import now, localtime

from croniter import croniter

from command_scheduler.models import Command as CommandModel
from command_scheduler.execution import execute_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        # create timings used to decide which command to run. this truly relies
        # on the fact cron is triggered every minute and slightly after the
        # exact minute
        this_run = localtime(now())
        last_run = this_run - timedelta(minutes=1)

        # get commands to run
        for command in CommandModel.objects.filter(enabled=True):
            # calculate the time the command should run next
            next_run = croniter(command.time, last_run).get_next(datetime)
            # if the command is not still running and should have been run
            if not command.is_running() and last_run < next_run < this_run:
                # do not share db connection with forked processes
                # this produce hard to debug problems
                connection.close()
                # for a process running the command
                Process(target=execute_command, args=[command.pk]).start()