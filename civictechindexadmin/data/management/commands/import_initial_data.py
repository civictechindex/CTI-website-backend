import csv
from django.core.management.base import BaseCommand
from ...models import Organization, Link


class Command(BaseCommand):
    help = ("Import data into our Organization and Link models. Requires you to provide a path to the data file.")

    def add_arguments(self, parser):
        # Positional arguments.
        parser.add_argument('filename')

    def handle(self, **options):
        with open(options['filename'], newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                org = self._create_organization(row)
                if org:
                    self._create_links(row, org)
                else:
                    continue

    def _create_organization(self, row):
        org, created = Organization.objects.get_or_create(name=row['organization_name'])
        org.import_id = row['ID']
        org.location = row['location']
        org.image_url = row['image_url']
        if row['ParentID']:
            parent = Organization.objects.filter(import_id=row['ParentID']).first()
            if parent:
                org.parent_organization = parent
            else:
                print(f"{row['organization_name']} had a parent id {row['ParentID']} but we did not find that organization")

        try:
            org.full_clean()
            org.save()
            return org
        except Exception as e:
            print('Problem creating or saving org')
            print(e)
            print(row)

    def _create_links(self, row, org):
        for field_name, option in [('website_link', 'WebSite'),
                                   ('meetup_link', 'MeetUp'),
                                   ('facebook_link', 'FaceBook'),
                                   ('twitter_link', 'Twitter'),
                                   ('github_link', 'GitHub')]:
            if row[field_name]:
                link, created = Link.objects.get_or_create(organization_id=org.id, link_type=option)
                link.url = row[field_name]
                try:
                    link.full_clean()
                    link.save()
                except Exception as e:
                    print('creating link failed')
                    print(e)
                    print(option, row[field_name])
                    continue
