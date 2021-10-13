## Collect all the tasks we want to run via django-q here
## https://django-q.readthedocs.io/en/latest/tasks.html
from django.core import management
from civictechindexadmin.data.management.commands import update_contributors


def update_contributors():
    management.call_command('update_contributors', verbosity=0)
