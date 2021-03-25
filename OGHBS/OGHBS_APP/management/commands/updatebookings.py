from django.core.management.base import BaseCommand, CommandError
from OGHBS_APP.models import *

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % "1"))