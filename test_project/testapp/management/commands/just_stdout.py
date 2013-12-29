from django.core.management import BaseCommand
from django.utils.timezone import now
import time
from optparse import make_option


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--switch',
            action='store_true',
            dest='switch',
            default=False,
            help='a switch for testing'),
        )

    def handle(self, *args, **options):
        self.stdout.write('Started "just_stdout" at %s' % now())
        print 'switch was ' + ('on' if options['switch'] else 'off')

        for i in range(30):
            print 'print #%d' % i
            time.sleep(1)

        self.stdout.write('Successfull end "just_stdout" at %s' % now())