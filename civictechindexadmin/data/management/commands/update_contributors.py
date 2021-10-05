# External Api Imports
from github import Github

# Django Imports
from django.conf import settings
from django.core.management.base import BaseCommand
from ...models import Link, Organization

# While it is possible to initialize Github() without passing in any access token, it is not reccomended,
# due to the fact that you will hit rate limit very fast.
git_api = Github(settings.GH_TOKEN)


def civictechindex_organizations_on_github(query='topic:civictechindex') -> dict:
    """Return a dictionary of organizations having repositories tagged with the topic `civictechindex`"""
    org_container = {}
    for repository in git_api.search_repositories(query):
        if repository.organization:
            org_container[repository.organization.name] = repository.organization

    if not org_container:
        raise Exception(f"No organizations found with the search query -> {query}")
    return org_container


def traverse_and_update(civictechindex_org_container):
    """
    Loops through all entries in the organization table and checks to see if that org matches any of
    the orgs found when querying GitHub for repositories tagged with `civictechindex` (API call above).

    In addition to setting the cti_contributor flag on organizations we already have in our
    database, we also want to be able to create new records for an organizations returned from our
    GitHub query that are not already in the Organization table. To do this, when we find a match
    between our org entries and the orgs in our GitHub data, we remove the item from the GitHub
    data. Then back in the 'handle' method, we check to see if there are left over orgs, and if so,
    we will add those organizations to our database as if they were "submitted" via the
    AddOrganization API.
    """
    org_names = civictechindex_org_container.keys()
    for org_in_db in Organization.objects.all():
        if org_in_db.name in org_names:
            civictechindex_org_container.pop(org_in_db.name)
            if not org_in_db.cti_contributor:
                org_in_db.cti_contributor = True
                org_in_db.save()
        else:
            if org_in_db.cti_contributor:
                org_in_db.cti_contributor = False
                org_in_db.save()


def add_new_organizations_to_db(organizations):
    """
    civictechindex_organizations_on_github found some orgs that were not already in our database,
    add them now with the status "submitted" so we can review them for inclusion.
    """
    for key, org in organizations.items():
        city = org.location if getattr(org, 'location') else ''
        new_org = Organization(
            name=org.name,
            # CNK the odd use of 'str' here is because one of the orgs lists its location as 'None'
            # which doesn't trigger the '' default but does violate the 'not null' contstraint
            city=city,
            image_url=getattr(org, 'avatar_url', ''),
            github_name=org.login,
            github_id=org.id,
            cti_contributor=True,
            status='submitted',
            # Fields that can be blank but not null
            state='',
            country='',
            organization_email='',
        )
        Organization.get_first_root_node().add_child(instance=new_org)
        # Add their GitHub URL (since we know it)
        gh_link = Link(organization=new_org, link_type='GitHub', url=org.url)
        gh_link.save()


class Command(BaseCommand):
    help = ("""
    This script queries the github api for all reposistories with the topic `civictechindex`.

    It then loops through the entire database organization table. If there is a matching orgnization
    name from the api call, we make sure the cti_contributor column is set to true. If we don't find
    a matching name in the orgs returned from our GH API call, we make sure the cti_contributor
    column is set to false.

    Lastly for any organizations from the api call that do not already exist in our db, it creates
    a new record for each discovered organization.

    NOTE: you will need a Personal Access Token from GitHub to run this script. Please use these
    instructions to create your own token, then set it in your environment as GH_TOKEN

    https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token
    """)

    def handle(self, **options):

        self.stdout.write('==========Script Start==========')

        query = 'topic:civictechindex'

        self.stdout.write(f'Creating a set of organizations that have the topic tag -> {query}')
        civictechindex_org_container = civictechindex_organizations_on_github(query)
        self.stdout.write(f'Successfully retrieved the following org -> {civictechindex_org_container.keys()}')

        self.stdout.write('Find civic tech organizations and update their cti_contributor column value')
        traverse_and_update(civictechindex_org_container)
        self.stdout.write(self.style.SUCCESS('Find and Update Complete'))

        if len(civictechindex_org_container) > 0:
            self.stdout.write(f'Add new organizations to database -> {civictechindex_org_container}')
            add_new_organizations_to_db(civictechindex_org_container)
            self.stdout.write('Add new organizations complete')

        self.stdout.write("==========Script End============")
