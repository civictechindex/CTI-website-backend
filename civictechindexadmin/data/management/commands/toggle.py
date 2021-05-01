# Python Imports
import os, logging
from datetime import datetime

# External Api Imports
from github import Github

# Django Imports
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from ...models import Organization


# Logger Configurations
logging.basicConfig(filename='manage_toggle.log',
                    level=logging.INFO,
                    format='%(levelname)s: %(asctime)s %(message)s')

# While it is possible to initialize Github() without passing in any access token, it is not reccomended,
# due to the fact that you will hit rate limit very fast.
git_api = Github(os.getenv('GH_TOKEN'))



def civictechindex_organizations_on_github() -> list:
    """Return a unique sorted list of organization names wich has the topic:civictechindex"""
    query = 'topic:civictechindex'
    org_container = set([repository.organization.name for repository in git_api.search_repositories(query) if repository.organization!=None])
    return sorted(org_container)

def create_issue_for_add_organization_to_db(organizations):
    logging.info(f'Created new issue for organization [{str(organizations)}]')

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

        logging.info('==========Script Start==========')     

        civictechindex_org_container = civictechindex_organizations_on_github()
        logging.info(f'civictechindex ogranizations from api call -> [{str(civictechindex_org_container)}]')
        all_orgs_in_db = Organization.objects.all()
        
        for org_in_db in all_orgs_in_db:
            if (org_in_db.name in civictechindex_org_container) and (org_in_db.cti_contributor == False):
                logging.info(f'org [{org_in_db.name}] in database exist in org name from api and db value is false, so it is being set to true')
                civictechindex_org_container.remove(org_in_db.name)  
                org_in_db.cti_contributor = True
                org_in_db.save()
            elif (org_in_db.name in civictechindex_org_container) and (org_in_db.cti_contributor == True):
                logging.info(f'org [{org_in_db.name}] in database exist in org name from api and db value is true, remove org from civictechindex_org_container')
                civictechindex_org_container.remove(org_in_db.name)
            elif (org_in_db.name not in civictechindex_org_container) and (org_in_db.cti_contributor == True):
                logging.info(f'org [{org_in_db.name}] in database does not exist in org name from api and db value is true, so it is being set to false')  
                org_in_db.cti_contributor = False
                org_in_db.save()

        create_issue_for_add_organization_to_db(civictechindex_org_container)

        logging.info('==========Script End==========')