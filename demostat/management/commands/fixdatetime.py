from django.core.management.base import BaseCommand, CommandError
from demostat.models import Demo
from django.utils import timezone
from pytz.exceptions import UnknownTimeZoneError
from django.conf import settings
from django.db import connection

import datetime
import math
import pytz
import time

class Command(BaseCommand):
    help = (
        'Re-localize objects from the given timezone.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'fromtz',
            type=str,
            help='The source-timezone you want to convert from'
        )

        parser.add_argument(
            '--noinput', '--no-input', action='store_false', dest='interactive',
            help='Tells Django to NOT prompt the user for input of any kind.',
        )

        parser.add_argument(
            '--dry-run', action='store_true', dest='dry_run',
            help='Do not save the changes.',
        )

    def handle(self, *args, **options):
        if not settings.USE_TZ:
            raise CommandError((
                'Django is running without USE_TZ settings.'
                ))

        self._fromtz = options['fromtz']
        self._desttz = settings.TIME_ZONE

        try:
            self.fromtz = pytz.timezone(self._fromtz)
            self.desttz = pytz.timezone(self._desttz)
        except UnknownTimeZoneError as e:
            raise CommandError('Timezone "%s" does not exist' % e)

        self.verbosity = options['verbosity']
        self.interactive = options['interactive']
        self.dry_run = options['dry_run']

        if self.interactive:
            confirm = input("""You have requested a update of the timezones.
This will IRREVERSIBLY ALTER all demos timezones
    Type 'yes' to continue, or 'no' to cancel: """)
        else:
            confirm = 'yes'

        if confirm == 'yes':
            demos = Demo.objects.all()
            self.start = time.perf_counter()

            if self.verbosity >= 1:
                self.stdout.write(self.style.MIGRATE_HEADING(
                        'Localizing {} demos from "{}" (shown in {})'.format(
                        len(demos),
                        self._fromtz,
                        self._desttz
                    ))
                )

            if self.verbosity >= 2:
                self.stdout.write(self.style.SQL_TABLE(
                    '{:9} {:^50} {:^{:d}} {:12} {:^25} {:^11} '.format(
                        '',
                        'demo.slug',
                        'id',
                        round(math.log(len(demos), 10)) + 2,
                        '',
                        'datetime in current TZ',
                        'offset'
                    )
                ))

            for demo in demos:
                _old = demo.date

                if self.verbosity >= 2:
                    self.stdout.write(
                        'Migrating {:>50} ({:{:d}d}) to timestamp '.format(
                            demo.slug, demo.id, round(math.log(len(demos), 10)), demo.date
                        ), ending=""
                    )

                demo.date = self.fromtz.localize(
                    demo.date.replace(tzinfo=None),
                    is_dst=None
                ).astimezone(self.desttz)

                if self.verbosity >= 2:
                    offset_str = offset = self.format_time_delta(_old - demo.date)

                    if _old > demo.date:
                        offset_str = self.style.SUCCESS(offset)
                    elif _old < demo.date:
                        offset_str = self.style.WARNING(offset)

                    self.stdout.write('{} ({}) '.format(
                        demo.date,
                        offset_str
                    ), ending="")

                if not self.dry_run:
                    demo.save(update_fields=['date'])

                    if self.verbosity >= 3:
                        print(connection.queries[-1])


                if self.verbosity >= 2:
                    self.stdout.write(self.style.SUCCESS('OK'))

            self.duration = ''

            if self.verbosity >= 2:
                self.stop = time.perf_counter()
                self.duration = f" in {self.stop - self.start:0.4f}s"

            if self.verbosity >= 1:
                self.stdout.write(self.style.MIGRATE_HEADING(
                    'Localized {} demos{}'.format(
                        len(demos),
                        self.duration
                    ))
                )

        else:
            self.stdout.write('Changing cancelled.')

    @staticmethod
    def format_time_delta(delta):
        """
        Format the given timedelta to a signed string with only
        hours, minutes and seconds displayed.

        >>> delta = datetime.timedelta(hours=-5)
        >>> format_time_delta(delta)
        '-05:00:00'
        >>> delta = datetime.timedelta(hours=+5,minutes=-30)
        >>> format_time_delta(delta)
        '+04:30:00'
        """

        positive = datetime.timedelta() < delta
        hours = divmod(delta.seconds, 60*60)
        minutes = divmod(hours[1], 60)
        seconds = minutes[1]

        #sign = '+' if positive else '-',

        if positive:
            sign = '+'
        elif datetime.timedelta() > delta:
            sign = '-'
        else:
            sign = u'\u00B1'

        return '{}{:02d}:{:02d}:{:02d}'.format(
                sign,abs(delta.days * 24 + hours[0]), minutes[0], seconds
            )
