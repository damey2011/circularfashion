from django.core.management import BaseCommand
from django.db.models import Q

from materials.models import AttributeOption, Attribute


class Command(BaseCommand):


    def handle(self, *args, **options):
        pass