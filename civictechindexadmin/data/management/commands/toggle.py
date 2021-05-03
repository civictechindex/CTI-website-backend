# Python Imports
import os, logging
from datetime import datetime

# External Api Imports
from github import Github

# Django Imports
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from ...models import Organization

# While it is possible to initialize Github() without passing in any access token, it is not reccomended,
# due to the fact that you will hit rate limit very fast.
git_api = Github(os.getenv('GH_TOKEN'))



def civictechindex_organizations_on_github(query = 'topic:civictechindex') -> list:
    """Return a unique sorted list of organization names wich has the topic:civictechindex"""
    org_container = set([repository.organization.name for repository in git_api.search_repositories(query) if repository.organization!=None])
    if len(org_container) == 0:
        raise Exception(f"No organization found with the search query -> {query}")
    return sorted(org_container)

def traverse_and_update(civictechindex_org_container):
    """Loops through all the objects within the organization table and update cti_contributor col"""
    for org_in_db in Organization.objects.all():
        if org_in_db.name in civictechindex_org_container:
            civictechindex_org_container.remove(org_in_db.name)
            if org_in_db.cti_contributor == False:
                org_in_db.cti_contributor = True
                org_in_db.save()
        else:
            if org_in_db.cti_contributor == True:
                org_in_db.cti_contributor = True
                org_in_db.save()

def add_new_organization_to_db(organizations):
    """Given a list of organizations name, add those organizations to the database while setting their cti_contributor col to True"""
    for org in organizations:
        Organization.get_first_root_node().add_child(instance=Organization(name=org,cti_contributor=True))
class Command(BaseCommand):
    help = ("""
    The toggle command queries the github api for all reposistories
    which has the topic:civictechindex. It loops through the entire 
    database organization table.

    For any matching orgnization name from the api call that exist in the database
        - it sets the cti_contributor column value to true

    For orgnization name in the database that does not exist in the rv of the api call
        - it sets the cti_contributor column value to true

    Lastly for any organization name from the api call that does not exist in the db
        - it creates a new github issue listing out the names of the organization that needs to be added to the db
    """)

    def handle(self, **options):

        self.stdout.write('==========Script Start==========')

        try:
            query = 'topic:civictechindex'

            self.stdout.write(f'Creating a set of organization that has the topic tag -> {query}')
            civictechindex_org_container = civictechindex_organizations_on_github(query)
            self.stdout.write(f'Successfully retrieved the following org -> {str(civictechindex_org_container)}')

            
            self.stdout.write(f'Find civic tech organizations and Update their cti_contributor colum value')
            traverse_and_update(civictechindex_org_container)
            self.stdout.write(self.style.SUCCESS(f'Find and Update Complete'))

            if len(civictechindex_org_container) > 0:
                self.stdout.write(f'Add new organizations to database that has the topic tag `civictechindex`-> {civictechindex_org_container}')
                add_new_organization_to_db(civictechindex_org_container)
                self.stdout.write(f'Add new organizations complete')
            
            self.stdout.write("==========Script End============")

        except Exception as error:
            self.stderr.write(error)
            


