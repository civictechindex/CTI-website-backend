from django.core.management.base import BaseCommand

from ...models import Organization, Organization2, Link2


class Command(BaseCommand):
    help = ("Move data to new Organization model. You may need to run this more than once to get all the leaf nodes created.")

    def handle(self, **options):
        # Start by copying the top level orgs
        root = Organization2.objects.filter(path='0001').first()
        if not root:
            root = Organization2(path='0001', name='Root')
            Organization2.add_root(instance=root)

        orgs = Organization.objects.prefetch_related('links', )
        for org in orgs.all():
            if org.parent_organization_id:
                try:
                    parent = Organization2.objects.get(import_id=org.parent_organization_id)
                except Organization2.DoesNotExist:
                    print(f'Parent {org.id} not found')
                    continue
            else:
                parent = root

            created = False
            new_org = Organization2.objects.filter(import_id=org.id).first()
            if not new_org:
                new_org = Organization2(import_id=org.id)
                created = True

            new_org.name = org.name
            new_org.city = org.city
            new_org.state = org.state
            new_org.country = org.country
            new_org.image_url = org.image_url
            new_org.github_name = org.github_name
            new_org.github_id = org.github_id
            new_org.cti_contributor = org.cti_contributor
            new_org.org_tag = org.org_tag

            if created:
                parent.add_child(instance=new_org)
            else:
                new_org.save()

            # Now add the links
            for link in org.links.all():
                new_link = Link2.objects.filter(link_type=link.link_type, organization_id=new_org.id).first()
                if not new_link:
                    new_link = Link2(link_type=link.link_type, organization_id=new_org.id)
                new_link.organization = new_org
                new_link.url = link.url
                new_link.http_status = link.http_status
                new_link.httt_status_date = link.http_status_date
                new_link.notes = link.notes
                new_link.save()
