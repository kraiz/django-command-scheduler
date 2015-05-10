from django.core.management.base import BaseCommand
from django.utils.timezone import now
import time


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--switch',
                            action='store_true',
                            dest='switch',
                            default=False,
                            help='a switch for testing')

    def handle(self, *args, **options):
        self.stdout.write('Started "just_stdout" at %s' % now())
        print('switch was ' + ('on' if options['switch'] else 'off'))

        for i in range(30):
            print('print #%d' % i)
            time.sleep(1)

        self.stdout.write('Successfull end "just_stdout" at %s' % now())