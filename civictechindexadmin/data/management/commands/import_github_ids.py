import json
from django.core.management.base import BaseCommand

from ...models import Organization


class Command(BaseCommand):
    help = ("Import github name and id data into our Organization model. "
            "Requires you to provide a path to the data file.")

    def add_arguments(self, parser):
        # Positional arguments.
        parser.add_argument('filename')

    def handle(self, **options):
        with open(options['filename'], newline='') as f:
            data = json.load(f)

        found = 0
        not_found = 0
        for item in data:
            o_by_ghname = Organization.objects.filter(github_name__iexact=item['name']).first()
            if o_by_ghname:
                found += 1
                if item['id']:
                    o_by_ghname.github_id = item['id']
                    o_by_ghname.save()
            else:
                not_found += 1
                print(item)

        print(f'Found: {found}')
        print(f'Not Found: {not_found}')
