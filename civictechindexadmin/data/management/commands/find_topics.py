# External Api Imports
from github import Github
from github.GithubException import UnknownObjectException

# Django Imports
from django.conf import settings
from django.core.management.base import BaseCommand
from ...models import Organization
from pprint import pprint


# While it is possible to initialize Github() without passing in any access token, it is not reccomended,
# due to the fact that you will hit rate limit very fast.
git_api = Github(settings.GH_TOKEN)



class Command(BaseCommand):
    help = ("""
    This script queries the github api for tags uses in all reposistories owned by organizations in our database.
    It then creates a file with the org, its repos, and all tags the org uses with counts for each tag.

    NOTE: you will need a Personal Access Token from GitHub to run this script. Please use these
    instructions to create your own token, then set it in your environment as GH_TOKEN

    https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token
    """)

    def handle(self, **options):
        output = {}
        for org_in_db in Organization.objects.filter(depth__gt=1).exclude(github_name='').all():
            try:
                org = git_api.get_organization(org_in_db.github_name)
            except UnknownObjectException:
                print(f'Could not find org {org_in_db.name} with GitHub name {org_in_db.github_name}')
            else:
                output[org_in_db.name] = {'repositories': [], 'topics': {}}
                for repo in org.get_repos(type='public'):
                    output[org_in_db.name]['repositories'].append(repo.full_name)
                    topics = repo.get_topics()
                    for topic in topics:
                        if output[org_in_db.name]['topics'].get(topic):
                            output[org_in_db.name]['topics'][topic] += 1
                        else:
                            output[org_in_db.name]['topics'][topic] = 1
                print(org_in_db.name)
                print([f'{key}: {count}' for key, count in output[org_in_db.name]['topics'].items() if count > 1])

